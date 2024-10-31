from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_GET

from illallangi.django.data.models import Model


@require_GET
def home_list(
    request: HttpRequest,
) -> render:
    base_template = "partial.html" if request.htmx else "base.html"

    return render(
        request,
        "home/home_list.html",
        {
            "object_count": Model.objects.get_object_count(),
            "model_count": Model.objects.count(),
            "base_template": base_template,
            "page": Paginator(
                object_list=sorted(
                    Model.objects.all(),
                    key=lambda x: x.singular,
                ),
                per_page=10,
            ).get_page(
                request.GET.get("page", 1),
            ),
            "links": [
                {
                    "rel": "alternate",
                    "type": "text/html",
                    "href": request.build_absolute_uri(
                        reverse(
                            "home_list",
                        ),
                    ),
                },
            ],
        },
    )
