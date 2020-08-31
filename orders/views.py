from django.http import JsonResponse
from .models import *
from django.shortcuts import render
from .forms import CheckoutContactForm
from django.contrib.auth.models import User


def basket_adding(request):
    return_dict = dict()
    session_key = request.session.session_key
    print(request.POST)
    data = request.POST
    product_id = data.get("product_id")
    nmb = data.get("nmb")
    is_delete = data.get("is_delete")

    if is_delete == 'true':
        ProductInBasket.objects.filter(id=product_id).update(is_active=False)
    else:
        new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key, product_id=product_id,
                                                                     is_active=True, order=None, defaults={"nmb": nmb})
        if not created:
            print("not created")
            new_product.nmb += int(nmb)
            new_product.save(force_update=True)

    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    products_total_nmb = products_in_basket.count()
    return_dict["products_total_nmb"] = products_total_nmb

    return_dict["products"] = list()

    for item in products_in_basket:
        product_dict = dict()
        product_dict["id"] = item.id
        product_dict["name"] = item.product.name
        product_dict["price"] = item.price
        product_dict["nmb"] = item.nmb
        return_dict["products"].append(product_dict)

    return JsonResponse(return_dict)


def checkout(request):
    session_key = request.session.session_key
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)

    form = CheckoutContactForm(request.POST or None)
    if request.POST:
        print(request.POST)

        if form.is_valid():
            print("yes")
            data = request.POST
            name = data.get("name", "noname")
            phone = data["phone"]
            payment = data["payment"]
            if payment == "Наличные":
                payment_id = 1
            else:
                payment_id = 2

            user, created = User.objects.get_or_create(username=phone, defaults={"first_name": name})

            order = Order.objects.create(user=user, client_name=name, client_phone=phone, payment_id=payment_id,
                                         status_id=1)  # создаем заказ

            for name, value in data.items():
                if name.startswith("product_in_basket_"):
                    product_in_basket_id = name.split("product_in_basket_")[1]  # считываем id
                    product_in_basket = ProductInBasket.objects.get(id=product_in_basket_id)  # по нему считываем товар

                    product_in_basket.nmb = value
                    product_in_basket.order = order
                    product_in_basket.save(force_update=True)

                    ProductInOrder.objects.create(product=product_in_basket.product, number=product_in_basket.nmb,
                                                  price=product_in_basket.price, amount=product_in_basket.amount,
                                                  order=order)

        else:
            print("no")
    return render(request, 'orders/checkout.html', locals())
