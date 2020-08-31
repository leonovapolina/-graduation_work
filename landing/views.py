from django.shortcuts import render
from .forms import SubscriberForm
from products.models import *


def landing(request):  # request - запрос из браузера
    form = SubscriberForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        print(request.POST)  # передаем данные
        print(form.cleaned_data)  # берем поля, которые нам нужны
        data = form.cleaned_data
        print(data["name"])  # смотрим имя

        new_form = form.save()  # сохраняем данные в бд (подписчики в админке)
    return render(request, 'landing/landing.html', locals())  # возвращает html шаблон, render - отрисовать


def home(request):
    products_photos = ProductPhoto.objects.filter(is_active=True, is_main=True, product__is_active=True)  # чтобы выводить продукты на сайте
    products_photos_berrymix = products_photos.filter(product__category_id=1)
    products_photos_strawberry = products_photos.filter(product__category_id=2)
    return render(request, 'landing/home.html', locals())
