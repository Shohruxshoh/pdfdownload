from django.db import models
import qrcode
import os
from django.core.files import File
from io import BytesIO


# Create your models here.

class PDF(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    file = models.FileField(upload_to='pdfs/')
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def __str__(self):
        return self.file.name

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None,
            *args, **kwargs
    ):
        self.title = self.file.name
        super(PDF, self).save(*args, **kwargs)
        if not self.qr_code:
            self.generate_qr_code()

    def generate_qr_code(self):
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(f'http://127.0.0.1:8000/download/{self.id}/')
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        self.qr_code.save(f'qr_code_{self.id}.png', File(buffer), save=False)
        super().save(update_fields=['qr_code'])
