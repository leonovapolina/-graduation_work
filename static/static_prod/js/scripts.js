$(document).ready(function(){
    var form = $('#form_buying_product');
    console.log(form);

    function basketUpdating(product_id, nmb, is_delete) {
        var data = {};  // данные, которые мы отправляем
        data.product_id = product_id;
        data.nmb = nmb;
        var csrf_token = $('#form_buying_product [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;  // чтобы django делать постзапрос

        if (is_delete) {
            data["is_delete"] = true;
        }

        var url = form.attr("action");  // адрес, на кот надо отправлять постзапрос
        console.log(data)
         $.ajax({
             url: url,
             type: 'POST',
             data: data,
             cache: true,
             success: function (data) {
                 console.log("OK");
                 console.log(data.products_total_nmb);
                 if (data.products_total_nmb || data.products_total_nmb == 0){
                     $('#basket_total_nmb').text("("+data.products_total_nmb+")");
                     console.log(data.products);
                     $('.basket-items ul').html("");  // при обновлении страницы мы очищаем отображение корзины
                     $.each(data.products, function(k, v){  // и для каждого товара выводим
                        $('.basket-items ul').append('<li>'+v.name+', '+v.nmb+' шт. по '+v.price+' руб. ' +
                            '<a class="delete-item" href="" data-product_id="'+v.id+'">x</a>' +
                            '</li>');
                     });
                 }
             },
             error: function(){
                 console.log("error")
             }
         })
    }

    $('.my-form').on('submit', function(e) {
        var form = $(this);
        e.preventDefault();  // чтобы элемент не исчезал а отображался в консоли
        var nmb = $(form.find('#number')).val();  // по id number получаем количество товара
        console.log(nmb);
        var submit_btn = $(form.find('#submit_btn'));  // по id на кнопке
        var product_id = submit_btn.data("product_id");  // получаем product_id
        var product_name = submit_btn.data("name");  // и name
        var product_price = submit_btn.data("price");
        console.log(product_id);
        console.log(product_name);
        console.log(product_price);

        basketUpdating(product_id, nmb, is_delete=false)
    });

    // form.on('submit', function(e) {
    //     e.preventDefault();  // чтобы элемент не исчезал а отображался в консоли
    //     var nmb = $('#number').val();  // по id number получаем количество товара
    //     console.log(nmb);
    //     var submit_btn = $('#submit_btn');  // по id на кнопке
    //     var product_id = submit_btn.data("product_id");  // получаем product_id
    //     var product_name = submit_btn.data("name");  // и name
    //     var product_price = submit_btn.data("price");
    //     console.log(product_id);
    //     console.log(product_name);
    //     console.log(product_price);
    //
    //     basketUpdating(product_id, nmb, is_delete=false)
    //
    //     // $('.basket-items ul').append('<li>'+product_name+', '+nmb+' шт. по '+product_price+' руб.   ' +
    //     //     // '<a class="delete-item" href="">x</a>' +
    //     //     '</li>');
    // });

    function showingBasket() {
         $('.basket-items').removeClass('hidden');  // удаляем либо добавляем класс hidden
    };

    $('.basket-container').on('click', function (e) {  // если мы нажимаем на корзину
        e.preventDefault();
        showingBasket()
    });

    $('.basket-container').mouseover(function () {  // если мы наводим на корзину
        showingBasket()
    });

    $('.basket-container').mouseout(function () {  // если мы убираем мышь с корзины
        $('.basket-items').addClass('hidden');
    });

    $(document).on('click', '.delete-item', function (e) {
        e.preventDefault();
        product_id = $(this).data("product_id")
        nmb = 0;
        basketUpdating(product_id, nmb, is_delete=true)
        //$(this).closest('li').remove();
    });

    function calculatingBasketAmount() {  // считаем сумму корзины
        var total_order_amount = 0
        $('.total-product-in-basket-amount').each(function () {
            total_order_amount += parseFloat($(this).text());
        });
        console.log(total_order_amount);
        $('#total_order_amount').text(total_order_amount.toFixed(2));
    };

    $(document).on('change', ".product-in-basket-nmb", function () {  // если мы меняем кол-во товара в корзине
        var current_nmb = $(this).val();  // берем текущее кол-во
        var current_tr = $(this).closest('tr');  // текущий ряд
        var current_price = parseFloat(current_tr.find('.product-price').text()).toFixed(2);  // ищем цену товара
        var total_amount = parseFloat(current_nmb * current_price).toFixed(2);  // пересчитываем общую цену товара
        current_tr.find('.total-product-in-basket-amount').text(total_amount);  // записываем в нужное поле таблицы

        calculatingBasketAmount();  // и вызовем функцию пересчета суммы корзины
    })

    calculatingBasketAmount();

});