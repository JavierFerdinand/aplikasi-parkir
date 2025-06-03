from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from parkir.models import SlotParkir
from parkir.views import *


@staff_member_required
def daftar_slot(request):
    slots = SlotParkir.objects.all().order_by('nomor_slot')
    return render(request, 'admintes/daftar_slot.html', {'slots': slots})

@staff_member_required
def checkout_slot_by_id(request, slot_id):
    slot = get_object_or_404(SlotParkir, id=slot_id)
    if request.method == 'POST':
        if not slot.tersedia:
            slot.tersedia = True
            slot.kode_unik = ''  # Kosongkan kode unik setelah checkout
            slot.save()
            messages.success(request, f"Slot {slot.nomor_slot} berhasil di-checkout.")
        else:
            messages.warning(request, f"Slot {slot.nomor_slot} sudah tersedia (belum dipakai).")
    return redirect('admintes:daftar_slot')

@staff_member_required
def checkout_slot_by_kode(request):
    if request.method == 'POST':
        kode_unik = request.POST.get('kode_unik')
        try:
            slot = SlotParkir.objects.get(kode_unik=kode_unik, tersedia=False)
            slot.tersedia = True
            slot.kode_unik = ''
            slot.save()
            messages.success(request, f"Slot {slot.nomor_slot} berhasil di-checkout dengan kode unik.")
        except SlotParkir.DoesNotExist:
            messages.error(request, "Kode unik tidak valid atau slot sudah di-checkout.")
    return redirect('admintes:daftar_slot')

@staff_member_required
def hapus_slot(request, slot_id):
    slot = get_object_or_404(SlotParkir, id=slot_id)
    if request.method == 'POST':
        slot.delete()
        messages.success(request, f"Slot {slot.nomor_slot} berhasil dihapus.")
    return redirect('admintes:daftar_slot')
