from django import forms
from .models import *


class SubscriberForm(forms.ModelForm):  # форма на основе модели Subscribers

    class Meta:
        model = Subscriber
        exclude = [""]  # ничего не исключаем
