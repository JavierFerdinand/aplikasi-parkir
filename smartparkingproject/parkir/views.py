
from django.shortcuts import get_object_or_404, render, redirect
from .models import SlotParkir, TiketParkir
from django.utils.timezone import now
import re


def index(request):
    slot_parkir = SlotParkir.objects.all()
    return render(request, 'parkir/index.html', {'slot_parkir': slot_parkir})

def slots(request, jenis):
    slot_tersedia = SlotParkir.objects.filter(jenis_kendaraan=jenis, tersedia=True)
    if request.method == "POST":
        slot_id = request.POST.get("slot_id")
        slot = SlotParkir.objects.get(id=slot_id)
        slot.tersedia = False
        slot.save()
        tiket = TiketParkir.objects.create(slot=slot)
        return redirect('struk', tiket_id=tiket.id)
    return render(request, 'parkir/slots.html', {'slots': slot_tersedia, 'jenis': jenis})

def struk(request, tiket_id):
    tiket = get_object_or_404(TiketParkir, id=tiket_id)
    return render(request, 'parkir/struk.html', {'tiket': tiket})

def home(request):
    slot_parkir = SlotParkir.objects.all()
    return render(request, 'home.html', {'slot_parkir': slot_parkir})
def kendaraan_masuk(request):
    data_kendaraan = TransaksiParkir.objects.all()
    return render(request, 'dashboard/kendaraan_masuk.html', {'data_kendaraan': data_kendaraan})

def natural_key(slot):
    # contoh nomor_slot: "A10" -> ("A", 10)
    match = re.match(r"([A-Za-z]+)(\d+)", slot.nomor_slot)
    if match:
        letter, number = match.groups()
        return (letter, int(number))
    else:
        return (slot.nomor_slot, 0)

def motor_view(request):
    slots = list(SlotParkir.objects.filter(jenis_kendaraan='motor').order_by('nomor_slot'))
    slots.sort(key=natural_key)
    half = len(slots) // 2
    slots_left = slots[:half]
    slots_right = slots[half:]
    context = {
        'slots_left': slots_left,
        'slots_right': slots_right,
    }
    return render(request, 'parkir/motor.html', context)


from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from .models import SlotParkir

def pilih_slot_motor(request, slot_id):
    slot = get_object_or_404(SlotParkir, id=slot_id, jenis_kendaraan='motor')

    if request.method == 'POST':
        if slot.tersedia:
            slot.tersedia = False
            slot.save()  # simpan perubahan ke DB

            waktu_pilih = now()
            context = {
                'slot': slot,
                'waktu_pilih': waktu_pilih,
            }
            return render(request, 'parkir/struk.html', context)
        else:
            # Slot sudah tidak tersedia, bisa redirect ke denah dengan pesan (optional)
            return redirect('motor')  # ganti dengan nama url denah motor
    else:
        return redirect('motor')  # ganti dengan nama url denah motor


def mobil_view(request):
    slots_mobil = SlotParkir.objects.filter(jenis_kendaraan='mobil')  # Ambil semua slot mobil
    return render(request, 'parkir/mobil.html', {'slots': slots_mobil})

def pilih_slot_mobil(request, slot_id):
    slot = get_object_or_404(SlotParkir, id=slot_id, jenis_kendaraan='mobil')
    if slot.tersedia:
        slot.tersedia = False
        slot.save()
    return redirect('mobil')

def checkout(request, pk):
    data = get_object_or_404(TransaksiParkir, pk=pk)
    data.sudah_checkout = True
    data.save()
    return redirect('kendaraan_masuk')
# Create your views here.
