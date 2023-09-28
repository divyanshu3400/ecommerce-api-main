from django import forms
from django.contrib import admin
from .models import FashionProduct, Color

# Register your models here.


from django.apps import apps

app_models = apps.get_app_config('ecommerce_app').get_models()
class ColorAdmin(admin.ModelAdmin):
    list_display = ('get_color_html', 'color_name')

admin.site.register(Color, ColorAdmin)

for model in app_models:
    if model !=Color:
        admin.site.register(model)
