from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat),
    path('ocr/', views.ocr),
    path('trend/', views.trend),
    path('search/<str:keyword>/', views.search),
    path('content/<path:encoded_url>/', views.content),
]