from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import PDFUploadForm
from .models import PDF
import os
from django.conf import settings


def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.title = form.files.get('file')
            form.save()
            return redirect('pdf_list')
    else:
        form = PDFUploadForm()
    return render(request, 'pdfupload/upload_pdf.html', {'form': form})


def pdf_list(request):
    pdfs = PDF.objects.all()
    return render(request, 'pdfupload/pdf_list.html', {'pdfs': pdfs})


def download_pdf(request, pdf_id):
    pdf = get_object_or_404(PDF, id=pdf_id)
    file_path = pdf.file.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    else:
        return HttpResponse(status=404)


def download_qr_code(request, pdf_id):
    pdf = get_object_or_404(PDF, id=pdf_id)
    file_path = pdf.qr_code.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="image/png")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    else:
        return HttpResponse(status=404)
