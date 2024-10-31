from django.core.management.base import BaseCommand

from illallangi.django.data.models import Synchronize


class Command(BaseCommand):
    help = "Description of your command"

    def handle(
        self,
        *_args: list[str],
        **_kwargs: dict[str, str],
    ) -> None:
        self.stdout.write("Starting synchronization:")

        for synchronize in Synchronize.objects.get_callables():
            self.stdout.write(f"Starting {synchronize.callable}:")
            synchronize.get_callable()()
            self.stdout.write(self.style.SUCCESS(f"Finished {synchronize.callable}."))

        self.stdout.write(self.style.SUCCESS("Finished synchronization."))
