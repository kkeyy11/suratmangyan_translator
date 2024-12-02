from django.urls import path
from . import views

urlpatterns = [
    path('', views.translate_image, name='translate_image'),
    path('translate/', views.translate_image, name='translate_image'),
    #path('history/', views.history, name='history'),  # New URL for History page
]
