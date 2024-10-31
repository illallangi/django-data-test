import importlib
from collections.abc import Generator
from typing import Any

from django.db import models


class ModelManager(
    models.Manager,
):
    def get_models(self) -> Generator[Any, None, None]:
        yield from [model.get_model() for model in self.all()]

    def get_object_count(self) -> int:
        return sum(model.count() for model in self.all())


class Model(
    models.Model,
):
    # Surrogate Keys

    id = models.AutoField(
        primary_key=True,
    )

    # Natural Keys

    model = models.CharField(
        blank=False,
        max_length=255,
        null=False,
        unique=True,
    )

    # Fields

    description = models.CharField(
        blank=False,
        max_length=255,
        null=False,
    )

    icon = models.CharField(
        blank=False,
        max_length=255,
        null=False,
    )

    plural = models.CharField(
        blank=False,
        max_length=255,
        null=False,
    )

    singular = models.CharField(
        blank=False,
        max_length=255,
        null=False,
    )

    url = models.CharField(
        blank=False,
        max_length=255,
        null=False,
    )

    objects = ModelManager()

    def __str__(self) -> str:
        return self.model

    def get_model(self) -> Any:  # noqa: ANN401
        name = self.model.split(".")[-1]
        module = importlib.import_module(
            self.model.removesuffix("." + name),
        )
        return getattr(module, name)

    def count(self) -> int:
        return self.get_model().objects.count()
