from django.http import JsonResponse
from categories.models import Category


def categories(req):
    all_categories = Category.objects.all()
    return JsonResponse(
        {
            "ok": True,
            # ERROR OCCUR: Object of type QuerySet is not JSON serializable
            # Need to translate(serialize) QuerySet to JSON
            "categories": all_categories,
        },
    )
