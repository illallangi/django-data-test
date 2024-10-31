from django.apps import AppConfig
from django.db.models.signals import post_migrate

from illallangi.django.data.signals import ready_for_models


def migration_complete(
    **_kwargs: dict[str, object],
) -> None:
    from illallangi.django.data.models import Model, Synchronize

    Model.objects.all().delete()
    Synchronize.objects.all().delete()

    ready_for_models.send(sender=DataConfig.__class__)


class DataConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "illallangi.django.data"

    def ready(
        self,
    ) -> None:
        post_migrate.connect(
            migration_complete,
            sender=self,
        )
        ready_for_models.send(self.__class__)
