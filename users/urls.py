from django.urls import path
from users import views


urlpatterns = [
    path("me", views.Me.as_view()),
]
