from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from parkir.models import SlotParkir
from django.contrib import messages

@staff_member_required
def daftar_slot(request):
    slots = SlotParkir.objects.all().order_by('nomor_slot')
    return render(request, 'admintes/daftar_slot.html', {'slots': slots})

@staff_member_required
def checkout_slot(request, slot_id):
    slot = get_object_or_404(SlotParkir, id=slot_id)
    if request.method == 'POST':
        slot.tersedia = True  # checkout berarti kosongkan slot
        slot.save()
        messages.success(request, f"Slot {slot.nomor_slot} berhasil di-checkout (tersedia kembali).")
    return redirect('admintes:daftar_slot')

@staff_member_required
def hapus_slot(request, slot_id):
    slot = get_object_or_404(SlotParkir, id=slot_id)
    if request.method == 'POST':
        slot.delete()
        messages.success(request, f"Slot {slot.nomor_slot} berhasil dihapus.")
    return redirect('admintes:daftar_slot')
