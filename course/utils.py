import os
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont

def generate_certificate_image(user, course, certificate_id, date):
    template_path = os.path.join(settings.BASE_DIR, 'course/static/images/certificate-template.jpg')
    output_folder = os.path.join(settings.MEDIA_ROOT, 'generated-certificates')
    
    os.makedirs(output_folder, exist_ok=True)

    # Open the template image
    certificate_image = Image.open(template_path)

    # Create a drawing object
    draw = ImageDraw.Draw(certificate_image)

    font_path = os.path.join(settings.BASE_DIR, 'course/static/fonts/Poppins-Light.ttf')
    font_size_name = 80
    font_size_course = 100
    font_size_id_date = 20

    name_font = ImageFont.truetype(font_path, font_size_name)
    course_font = ImageFont.truetype(font_path, font_size_course)
    id_date_font = ImageFont.truetype(font_path, font_size_id_date)

    center_x = certificate_image.width // 2


    name_text = user
    name_width, name_height = draw.textsize(name_text, font=name_font)
    name_x = center_x - name_width // 2
    name_y = 1400
    draw.text((name_x, name_y), name_text, fill=(128, 0, 0), font=name_font)

    # Print the name of the course (center aligned in X-axis and Y-axis 800)
    course_text = course
    course_width, course_height = draw.textsize(course_text, font=course_font)
    course_x = center_x - course_width // 2
    course_y = 800
    draw.text((course_x, course_y), course_text, fill="black", font=course_font)

    # Print the certificate ID (center aligned in X-axis and Y-axis 2491)
    id_text = f"Certificate ID: {certificate_id}"
    id_width, id_height = draw.textsize(id_text, font=id_date_font)
    id_x = center_x - id_width // 2
    id_y = 2491
    draw.text((id_x, id_y), id_text, fill="black", font=id_date_font)

    # Print the date (center aligned in X-axis and Y-axis 2511)
    date_text = f"Date: {date}"
    date_width, date_height = draw.textsize(date_text, font=id_date_font)
    date_x = center_x - date_width // 2
    date_y = 2511
    draw.text((date_x, date_y), date_text, fill="black", font=id_date_font)

    # Save the modified certificate image
    certificate_filename = f"Certificate_{user}_{course}.jpg"
    output_path = os.path.join(output_folder, certificate_filename)
    certificate_image.save(output_path)
    return output_path
