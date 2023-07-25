import os
import cv2
from datetime import datetime

def generate_certificate_image(name, course_name, certificate_id):
    template_path = "certificate-template.jpg"
    output_folder = "generated-certificates/"
    os.makedirs(output_folder, exist_ok=True)

    certificate_image = cv2.imread(template_path)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.2
    font_thickness = 2
    text_color = (0, 0, 0) 

    (name_width, name_height), _ = cv2.getTextSize(name, font, font_scale, font_thickness)
    name_position_x = int((certificate_image.shape[1] - name_width) / 2)
    name_position_y = int(certificate_image.shape[0] * 0.4)


    cv2.putText(certificate_image, name, (name_position_x, name_position_y), font, font_scale, text_color, font_thickness,
                cv2.LINE_AA)


    (course_width, course_height), _ = cv2.getTextSize(course_name, font, font_scale, font_thickness)
    course_position_x = int((certificate_image.shape[1] - course_width) / 2)
    course_position_y = int(certificate_image.shape[0] * 0.6)


    cv2.putText(certificate_image, course_name, (course_position_x, course_position_y), font, font_scale, text_color, font_thickness,
                cv2.LINE_AA)


    certificate_id_date = f"Certificate ID: {certificate_id} - {datetime.now().strftime('%Y-%m-%d')}"
    (id_date_width, id_date_height), _ = cv2.getTextSize(certificate_id_date, font, 0.6, font_thickness)
    id_date_position_x = int((certificate_image.shape[1] - id_date_width) / 2)
    id_date_position_y = int(certificate_image.shape[0] * 0.9)


    cv2.putText(certificate_image, certificate_id_date, (id_date_position_x, id_date_position_y), font, 0.6, text_color, font_thickness,
                cv2.LINE_AA)

    output_path = os.path.join(output_folder, f"{name}_certificate.jpg")
    cv2.imwrite(output_path, certificate_image)
    print(f"Certificate generated for {name} - Certificate ID: {certificate_id} - Date: {datetime.now().strftime('%Y-%m-%d')}")
