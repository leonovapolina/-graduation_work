from django import forms


class CheckoutContactForm(forms.Form):  # форма без привязки к модели
    name = forms.CharField(required=True, error_messages={'required': 'Пожалуйста, укажите имя'})
    phone = forms.CharField(required=True, error_messages={'required': 'Пожалуйста, укажите номер телефона'})
    payment = forms.CharField(required=True)
