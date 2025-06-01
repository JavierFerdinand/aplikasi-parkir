# parkir/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('slots/<str:jenis>/', views.slots, name='slots'),
    path('struk/<int:tiket_id>/', views.struk, name='struk'),
]