# parkir/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('slots/<str:jenis>/', views.slots, name='slots'),
    path('struk/<int:tiket_id>/', views.struk, name='struk'),
    path('motor/', views.motor_view, name='motor'),
    path('pilih-slot-motor/<int:slot_id>/', views.pilih_slot_motor, name='pilih_slot_motor'),
    path('mobil/', views.mobil_view, name='mobil'),
    path('pilih-slot-mobil/<int:slot_id>/', views.pilih_slot_mobil, name='pilih_slot_mobil'),
    
    
]