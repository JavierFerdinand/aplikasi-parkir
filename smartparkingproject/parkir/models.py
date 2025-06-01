from django.db import models
import uuid

class SlotParkir(models.Model):
    JENIS_KENDARAAN = [('mobil', 'Mobil'), ('motor', 'Motor')]
    nomor_slot = models.CharField(max_length=10)
    jenis_kendaraan = models.CharField(max_length=10, choices=JENIS_KENDARAAN)
    tersedia = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nomor_slot} - {self.jenis_kendaraan}"

class TiketParkir(models.Model):
    slot = models.ForeignKey(SlotParkir, on_delete=models.CASCADE)
    kode_unik = models.UUIDField(default=uuid.uuid4, editable=False)
    waktu_masuk = models.DateTimeField(auto_now_add=True)

# Create your models here.
