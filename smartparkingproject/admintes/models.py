from django.db import models

class SlotParkir(models.Model):
    nomor_slot = models.CharField(max_length=10)
    jenis_kendaraan = models.CharField(max_length=20)
    tersedia = models.BooleanField(default=True)
    kode_unik = models.CharField(max_length=100, blank=True, null=True)  # ← wajib ada
