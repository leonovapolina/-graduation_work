from django.contrib import admin
from .models import *


class ProductPhotoInline(admin.TabularInline):  # чтобы вкладывать в другие страницы на админке
    model = ProductPhoto
    extra = 0  # отображение рядов только если есть картинки


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductCategory._meta.fields]

    class Meta:
        model = ProductCategory


admin.site.register(ProductCategory, ProductCategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]
    inlines = [ProductPhotoInline]  # вкладываем как раз

    class Meta:
        model = Product


admin.site.register(Product, ProductAdmin)


class ProductPhotoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductPhoto._meta.fields]

    class Meta:
        model = ProductPhoto


admin.site.register(ProductPhoto, ProductPhotoAdmin)
