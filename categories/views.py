from django.http import JsonResponse
from django.core import serializers
from categories.models import Category


def categories(req):
    all_categories = Category.objects.all()
    return JsonResponse(
        {
            "ok": True,
            "categories": serializers.serialize("json", all_categories),
        },
    )
