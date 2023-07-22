# views.py

from django.shortcuts import render
from django.http import HttpResponse
from .models import Certificate

def home(request):
    # Assuming you want to retrieve and display certificates for the currently logged-in user
    user = request.user

    # Fetch certificates for the logged-in user
    certificates = Certificate.objects.filter(user=user)

    # You can also generate certificates here if needed
    for certificate in certificates:
        certificate.generate_certificate()

    return render(request, 'home.html', {'certificates': certificates})
