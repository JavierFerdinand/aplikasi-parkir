from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'admintes'

urlpatterns = [
    path('slots/', views.daftar_slot, name='daftar_slot'),
    path('slots/checkout/<int:slot_id>/', views.checkout_slot_by_id, name='checkout_slot_by_id'),
    path('slots/hapus/<int:slot_id>/', views.hapus_slot, name='hapus_slot'),
    path('slots/checkout/', views.checkout_slot_by_kode, name='checkout_slot_by_kode'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/admin/'), name='logout'),
]
