from typing import Any

from django import template

register = template.Library()


@register.filter
def breadcrumbs_title(
    breadcrumbs: list[Any],
    suffix: str = "data.coley.au",
) -> str:
    return " - ".join(
        [str(breadcrumb["title"]) for breadcrumb in reversed(breadcrumbs)] + [suffix]
    )
