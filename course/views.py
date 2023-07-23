
import os
import cv2
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Certificate


@login_required
def generate_certificates(request):
    user = request.user
    if user.is_authenticated and user.is_premium_member:  # Adjust this condition based on your User model
        name = user.username  # You can modify this to include other users' names as well

        template_path = "certificate-template.jpg"  # Replace this with the path to your certificate template image
        certificate_image = cv2.imread(template_path)

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 5
        font_thickness = 10
        text_color = (0, 0, 0)  # Black color

        (text_width, text_height), _ = cv2.getTextSize(name, font, font_scale, font_thickness)
        position_x = int((certificate_image.shape[1] - text_width) / 2)
        position_y = int((certificate_image.shape[0] + text_height) / 2)

        cv2.putText(certificate_image, name, (position_x, position_y), font, font_scale, text_color, font_thickness,
                    cv2.LINE_AA)

        certificate = Certificate.objects.create(user=user, certificate_file="path/to/certificate/in/s3")

        print("Certificate generated and saved!")

        return HttpResponse("Certificate generated and saved successfully!")

    return HttpResponse("You are not a premium member or not logged in.")
