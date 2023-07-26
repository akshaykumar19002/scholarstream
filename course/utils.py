import os
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont

def generate_certificate_image(user, course, certificate_id, date):
    template_path = os.path.join(settings.BASE_DIR, 'course/static/images/certificate-template.jpg')
    output_folder = os.path.join(settings.MEDIA_ROOT, 'generated-certificates')
    
    os.makedirs(output_folder, exist_ok=True)

    certificate_image = Image.open(template_path)
    draw = ImageDraw.Draw(certificate_image)

    font_path = "Poppins-Light.ttf"
    font_size_name = 80
    font_size_course = 100
    font_size_id_date = 20

    font_name = ImageFont.truetype(font_path, font_size_name)
    font_course = ImageFont.truetype(font_path, font_size_course)
    font_id_date = ImageFont.truetype(font_path, font_size_id_date)

    img_width, img_height = certificate_image.size

    position_x_name = int(img_width / 2)
    position_x_course = int(img_width / 2)
    position_x_id_date = int(img_width / 2)
    position_y_name = 700
    position_y_course = 800

    position_y_id_date = 2491

    draw.text((position_x_name, position_y_name), user.full_name, fill=(128, 0, 0), font=font_name, anchor="mm")

    draw.text((position_x_course, position_y_course), course.name, fill=(0, 0, 0), font=font_course, anchor="mm")

    draw.text((position_x_id_date, position_y_id_date), f"Certificate ID: {certificate_id}", fill=(0, 0, 0), font=font_id_date, anchor="mm")
    draw.text((position_x_id_date, position_y_id_date + 20), f"Date: {date}", fill=(0, 0, 0), font=font_id_date, anchor="mm")

    output_path = os.path.join(output_folder, f"{user}_{course}_certificate.jpg")
    certificate_image.save(output_path)
    return output_path
