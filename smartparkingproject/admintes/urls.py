from django.urls import path
from . import views

app_name = 'admintes'

urlpatterns = [
    path('slots/', views.daftar_slot, name='daftar_slot'),
    path('slots/checkout/<int:slot_id>/', views.checkout_slot_by_id, name='checkout_slot_by_id'),
    path('slots/hapus/<int:slot_id>/', views.hapus_slot, name='hapus_slot'),
    path('slots/checkout/', views.checkout_slot_by_kode, name='checkout_slot_by_kode'),
]
