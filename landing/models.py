# модель - описание полей в таблице бд
from django.db import models


class Subscriber(models.Model):
    email = models.EmailField()  # поле модели под почту
    name = models.CharField(max_length=128)  # и имя

    def __str__(self):  # будем отображать данные в полях админки
        return "Пользователь %s %s" % (self.name, self.email)

    class Meta:  # сами задаем произносимое имя
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
