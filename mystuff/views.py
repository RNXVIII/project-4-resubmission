# Create your views here.
from django.shortcuts import render

def myprofile(request):
    return render(request, 'mystuff/myprofile.html') 