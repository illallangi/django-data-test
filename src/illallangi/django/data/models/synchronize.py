import importlib
from collections.abc import Callable, Generator
from typing import Any

from django.db import models
from toposort import toposort_flatten


class SynchronizeManager(
    models.Manager,
):
    def get_callables(self) -> Generator[Callable[..., Any]]:
        for c in toposort_flatten(
            {
                s.callable: [
                    *s.after,
                    *[t.callable for t in self.all() if s.callable in t.before],
                ]
                for s in self.all()
            },
        ):
            yield self.get(callable=c)


class Synchronize(
    models.Model,
):
    # Surrogate Keys

    id = models.AutoField(
        primary_key=True,
    )

    # Natural Keys

    callable = models.CharField(
        blank=False,
        max_length=255,
        null=False,
        unique=True,
    )

    # Fields

    after = models.JSONField(
        blank=False,
        default=list,
        null=False,
    )

    before = models.JSONField(
        blank=False,
        default=list,
        null=False,
    )

    objects = SynchronizeManager()

    def __str__(self) -> str:
        return self.callable

    def get_callable(self) -> Callable[..., Any]:
        name = self.callable.split(".")[-1]
        module = importlib.import_module(
            self.callable.removesuffix("." + name),
        )
        return getattr(module, name)
