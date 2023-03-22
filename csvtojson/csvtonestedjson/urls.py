from django.urls import path
from . import views

urlpatterns = [
    path('', views.FileOperation.as_view()),
]
