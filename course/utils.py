import os
import cv2
from django.conf import settings
from .models import Certificate

def generate_certificate_image(name):
    template_path = os.path.join(settings.STATIC_ROOT, 'static/images/certificate-template.jpg')
    output_folder = os.path.join(settings.MEDIA_ROOT, 'generated-certificates')
    os.makedirs(output_folder, exist_ok=True)

    certificate_image = cv2.imread(template_path)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 5
    font_thickness = 10
    text_color = (0, 0, 0)


    (text_width, text_height), _ = cv2.getTextSize(name, font, font_scale, font_thickness)
    position_x = int((certificate_image.shape[1] - text_width) / 2)
    position_y = int((certificate_image.shape[0] + text_height) / 2)


    cv2.putText(certificate_image, name, (position_x, position_y), font, font_scale, text_color, font_thickness,
                cv2.LINE_AA)

    output_path = os.path.join(output_folder, f"{name}.jpg")
    cv2.imwrite(output_path, certificate_image)
    return output_path


def generate_certificate(user, course):
    if user.is_subscribed:
        certificate_image_path = generate_certificate_image(user.full_name)
        certificate = Certificate(user=user, course=course, certificate_image=certificate_image_path)
        certificate.save()
