from django.contrib.admin import ModelAdmin, register

from illallangi.django.data.models import Model


@register(Model)
class ModelAdmin(ModelAdmin):
    pass
