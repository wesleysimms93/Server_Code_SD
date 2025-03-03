

# Create your views here.
from django.shortcuts import render

def printer_control(request):
    return render(request, 'wifi/3d_printer.html')

