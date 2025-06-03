
from django.shortcuts import get_object_or_404, render, redirect
from .models import SlotParkir, TiketParkir, LogTransaksi
from django.utils.timezone import now
import re
import io
import base64
import barcode
from barcode.writer import ImageWriter

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



def natural_key(slot):
    # contoh nomor_slot: "A10" -> ("A", 10)
    match = re.match(r"([A-Za-z]+)(\d+)", slot.nomor_slot)
    if match:
        letter, number = match.groups()
        return (letter, int(number))
    else:
        return (slot.nomor_slot, 0)

def motor_view(request):
    # Get all motorcycle slots ordered by natural key
    slots = list(SlotParkir.objects.filter(jenis_kendaraan='motor').order_by('nomor_slot'))
    slots.sort(key=natural_key)
    
    # Split into left and right sides
    half = len(slots) // 2
    slots_left = slots[:half]
    slots_right = slots[half:]
    
    # Group into rows (5 slots per row - adjust this number as needed)
    def chunk(lst, n):
        """Split list into chunks of size n"""
        return [lst[i:i + n] for i in range(0, len(lst), n)]
    
    # Organize into rows for the template
    slots_left_rows = chunk(slots_left, 6)  # 5 slots per row on left side
    slots_right_rows = chunk(slots_right, 6)  # 5 slots per row on right side
    
    context = {
        'slots_left': slots_left_rows,  # Now a list of lists (rows)
        'slots_right': slots_right_rows,  # Now a list of lists (rows)
    }
    return render(request, 'parkir/motor.html', context)

def pilih_slot_motor(request, slot_id):
    slot = get_object_or_404(SlotParkir, id=slot_id, jenis_kendaraan='motor')

    if request.method == 'POST':
        if slot.tersedia:
            slot.tersedia = False
            slot.save()

            tiket = TiketParkir.objects.create(slot=slot)
            return redirect('struk', tiket_id=tiket.id)
        else:
            return redirect('motor')
    else:
        return redirect('motor')


def mobil_view(request):
    slots = list(SlotParkir.objects.filter(jenis_kendaraan='mobil').order_by('nomor_slot'))
    slots.sort(key=natural_key)
    
    half = len(slots) // 2
    slots_left = slots[:half]
    slots_right = slots[half:]
    
    
    def chunk(lst, n):
        """Split list into chunks of size n"""
        return [lst[i:i + n] for i in range(0, len(lst), n)]
    
    slots_left_rows = chunk(slots_left, 3)  
    slots_right_rows = chunk(slots_right, 3)  
    
    context = {
        'slots_left': slots_left_rows,  
        'slots_right': slots_right_rows,  
    }
    return render(request, 'parkir/mobil.html', context)


def pilih_slot_mobil(request, slot_id):
    slot = get_object_or_404(SlotParkir, id=slot_id, jenis_kendaraan='mobil')

    if request.method == 'POST':
        if slot.tersedia:
            slot.tersedia = False
            slot.save()

            tiket = TiketParkir.objects.create(slot=slot)
            return redirect('struk', tiket_id=tiket.id)
        else:
            return redirect('mobil')
    else:
        return redirect('mobil')


def checkout(request, pk):
    data = get_object_or_404(TransaksiParkir, pk=pk)
    data.sudah_checkout = True
    data.save()
    return redirect('kendaraan_masuk')

def struk(request, tiket_id):
    tiket = get_object_or_404(TiketParkir, id=tiket_id)
    kode_unik = tiket.slot.kode_unik  # ambil kode unik dari slot

    # Generate barcode Code39
    CODE39 = barcode.get_barcode_class('code39')

    buffer = io.BytesIO()
    barcode_obj = CODE39(kode_unik, writer=ImageWriter(), add_checksum=False)
    barcode_obj.write(buffer)

    barcode_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return render(request, 'parkir/struk.html', {
        'tiket': tiket,
        'waktu_pilih': tiket.waktu_masuk,
        'barcode_base64': barcode_base64,  # kirim ke template
    })

def slots(request, jenis):
    slot_tersedia = SlotParkir.objects.filter(jenis_kendaraan=jenis, tersedia=True)
    if request.method == "POST":
        slot_id = request.POST.get("slot_id")
        slot = SlotParkir.objects.get(id=slot_id)
        slot.tersedia = False
        slot.save()
        
        tiket = TiketParkir.objects.create(slot=slot)
        
        LogTransaksi.objects.create(tiket=tiket, aksi="Slot dipesan")

        return redirect('struk', tiket_id=tiket.id)
    return render(request, 'parkir/slots.html', {'slots': slot_tersedia, 'jenis': jenis})

