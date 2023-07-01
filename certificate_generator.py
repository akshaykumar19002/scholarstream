import os
import cv2


def delete_previous_certificates():
    folder_path = "generated-certificates/"
    if os.path.exists(folder_path):
        file_list = os.listdir(folder_path)
        for file_name in file_list:
            file_path = os.path.join(folder_path, file_name)
            os.remove(file_path)


def load_names_from_file():
    names = []
    with open('name-data.txt', 'r') as file:
        for line in file:
            name = line.strip()
            names.append(name)
    return names


def generate_certificates(names):
    template_path = "certificate-template.jpg"
    output_folder = "generated-certificates/"
    os.makedirs(output_folder, exist_ok=True)

    for index, name in enumerate(names, start=1):
        certificate_image = cv2.imread(template_path)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 5
        font_thickness = 10
        text_color = (0, 0, 0)  # Black color

        # Get the text size for centering the text
        (text_width, text_height), _ = cv2.getTextSize(name, font, font_scale, font_thickness)
        position_x = int((certificate_image.shape[1] - text_width) / 2)
        position_y = int((certificate_image.shape[0] + text_height) / 2)

        # Draw the text on the image
        cv2.putText(certificate_image, name, (position_x, position_y), font, font_scale, text_color, font_thickness,
                    cv2.LINE_AA)

        output_path = os.path.join(output_folder, f"{name}.jpg")
        cv2.imwrite(output_path, certificate_image)
        print(f"Processing {index} / {len(names)}")


def main():
    delete_previous_certificates()
    names = load_names_from_file()
    generate_certificates(names)


if __name__ == '__main__':
    main()
