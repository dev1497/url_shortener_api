from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('short_url/', views.shorten_url,  name='short_url'),
    path('<str:short_url>', views.get_url, name='get_url'),
]