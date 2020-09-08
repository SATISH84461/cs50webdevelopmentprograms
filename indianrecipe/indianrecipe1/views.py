from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def menu(request):
    return render(request, 'menu.html')

def contact(request):
    return render(request, 'contact.html')

def aboutus(request):
    return render(request, 'aboutus.html')
    
# Create your views here.
