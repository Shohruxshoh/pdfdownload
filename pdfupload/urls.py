from django.urls import path
from .views import upload_pdf, pdf_list, download_pdf, download_qr_code

urlpatterns = [
    path('', pdf_list, name='pdf_list'),
    path('upload/', upload_pdf, name='upload_pdf'),
    path('download/<int:pdf_id>/', download_pdf, name='download_pdf'),
    path('download_qr/<int:pdf_id>/', download_qr_code, name='download_qr_code'),
]


