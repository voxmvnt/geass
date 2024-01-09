from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('about_engineer/', views.about_engineer),
    path('login/', views.login),
]