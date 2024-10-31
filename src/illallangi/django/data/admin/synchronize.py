from django.contrib.admin import ModelAdmin, register

from illallangi.django.data.models import Synchronize


@register(Synchronize)
class SynchronizeAdmin(ModelAdmin):
    pass
