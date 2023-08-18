import io
import PyPDF2
from PIL import Image
from django.http import HttpResponse
from django.shortcuts import render
from io import BytesIO
from PIL import Image as PilImage
import pdfrw


def add_password(request):
	title = "Add password"
	if request.method == 'POST':
	
		pdf_file = request.FILES['pdf_file']
		password = request.POST['password']
		
		pdf_in = PyPDF2.PdfReader(pdf_file)
		pdf_file = PyPDF2.PdfWriter()
		
		for page in pdf_in.pages:
			pdf_file.add_page(page)
		
		pdf_file.encrypt(password)
		
		pdf_output = BytesIO()
		pdf_file.write(pdf_output)
		# with open('encrypted.pdf', 'wb') as f:
		# 	pdf_file.write(f)
		response = HttpResponse(pdf_output.getvalue(), content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename='"encrypted.pdf"
		return response
	
	context = {
		'title': title,
	}
	return render(request, 'helper/add_password.html', context)


def delete_metadata(request):
	title = "Delete Metadata"
	if request.method == 'POST':
		pdf_file = request.FILES['pdf_file']
		pdf_in = PyPDF2.PdfReader(pdf_file)
		pdf_out = PyPDF2.PdfWriter()
		
		for page in pdf_in.pages:
			pdf_out.add_page(page)
		
		pdf_out.remove_links()
		
		pdf_bytes = BytesIO()
		pdf_out.write(pdf_bytes)
		pdf_bytes.seek(0)
		
		pdf = pdfrw.PdfReader(pdf_bytes)
		pdf.Info = pdfrw.IndirectPdfDict()
		
		result_pdf = BytesIO()
		pdfrw.PdfWriter().write(result_pdf, pdf)
		
		response = HttpResponse(result_pdf.getvalue(), content_type = 'application/pdf')
		response['Content-Disposition'] = 'attachment; filename="modified.pdf"'
		return response
	
	context = {
		'title': title,
	}
	return render(request, 'helper/delete_metadata.html', context)


def add_image_signature(pdf_file, signature_image):
	input_pdf = PyPDF2.PdfReader(pdf_file)
	first_page = input_pdf.pages[0]
	
	pdf_writer = PyPDF2.PdfWriter()
	pdf_writer.add_page(first_page)
	
	signature_image_obj = PilImage.open(signature_image)
	
	signature_bytes = io.BytesIO()
	signature_image_obj.save(signature_bytes, format = 'PNG')
	signature_image_bytes = signature_bytes.getvalue()
	
	signature_image_obj = Image.open(io.BytesIO(signature_image_bytes))
	
	input_pdf.addImage(signature_image_obj, 0, 0, 100, 100)
	
	output = PyPDF2.PdfFileWriter()
	output.addPage(input_pdf.getPage(0))
	
	signed_pdf = io.BytesIO()
	output.write(signed_pdf)
	
	signed_pdf.seek(0)
	
	return signed_pdf


def add_signature(request):
	title = "Add Signature"
	if request.method == 'POST':
		pdf_file = request.FILES['pdf_file']
		signature_image = request.FILES['image_signature']
		
		signed_pdf = add_image_signature(pdf_file, signature_image)
		response = HttpResponse(signed_pdf, content_type = 'application/pdf')
		response['Content-Disposition'] = 'attachment; filename="signed_pdf"'
		return response
	context = {
		'title': title,
	}
	return render(request, 'helper/add_signature.html', context)


def optimize_file(request):
	title = "Optimize File"
	
	context = {
		'title': title,
	}
	return render(request, 'helper/optimize_file.html', context)

