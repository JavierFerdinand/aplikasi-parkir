from django.db import models
import uuid

class SlotParkir(models.Model):
    JENIS_KENDARAAN = [('mobil', 'Mobil'), ('motor', 'Motor')]
    nomor_slot = models.CharField(max_length=10)
    jenis_kendaraan = models.CharField(max_length=10, choices=JENIS_KENDARAAN)
    tersedia = models.BooleanField(default=True)
    kode_unik = models.CharField(max_length=20, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.kode_unik:
            self.kode_unik = uuid.uuid4().hex[:8].upper()  
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.nomor_slot} - {self.jenis_kendaraan}"

class TiketParkir(models.Model):
    slot = models.ForeignKey(SlotParkir, on_delete=models.CASCADE)
    waktu_masuk = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tiket {self.kode_unik} untuk slot {self.slot.nomor_slot}" 
    

class LogTransaksi(models.Model):
    tiket = models.ForeignKey(TiketParkir, on_delete=models.CASCADE)
    waktu_log = models.DateTimeField(auto_now_add=True)
    aksi = models.CharField(max_length=100)  #gajadi dipake

    def __str__(self):
        return f"{self.waktu_log} - {self.aksi} - {self.tiket.kode_unik}"
