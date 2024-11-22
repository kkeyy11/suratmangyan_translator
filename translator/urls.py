from django.urls import path
from .views import translate_image
from . import views

urlpatterns = [
    path('', translate_image, name='translate_image'),
    path('translate/', views.translate_image, name='translate_image'),
]
