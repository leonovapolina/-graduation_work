from django.contrib import admin
from .models import *


class SubscriberAdmin (admin.ModelAdmin):
    # list_display = ["name", "email"]  # какие поля выводим
    list_display = [field.name for field in Subscriber._meta.fields]  # все поля
    # exclude = ["email"]  # что хотим исключить (не показывать)
    # fields = ["email"]  # что показываем
    list_filter = ['name',]  # справа фильтр по полю
    search_fields = ['name', 'email']  # поиск по имени или почте

    class Meta:
        model = Subscriber


admin.site.register(Subscriber, SubscriberAdmin)
# регистрируем модель (SubscriberAdmin перекроет то, что написано в модели)
