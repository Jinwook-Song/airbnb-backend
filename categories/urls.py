from django.urls import path
from categories import views

# https://www.django-rest-framework.org/api-guide/viewsets/#viewset-actions
urlpatterns = [
    path(
        "",
        views.CategoryViewSet.as_view(
            # connect http methods and class methods
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "<int:pk>",
        views.CategoryViewSet.as_view(
            {
                "get": "retrieve",
                "put": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
]
