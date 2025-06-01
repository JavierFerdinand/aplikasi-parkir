
from django.shortcuts import render, get_object_or_404, redirect
from .models import SlotParkir, TiketParkir

def index(request):
    return render(request, 'parkir/index.html')

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
# Create your views here.
