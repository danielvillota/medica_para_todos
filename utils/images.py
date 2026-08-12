import base64
from django.contrib.staticfiles import finders

def get_static_image_base64(static_path):
    """
    Convierte una imagen ubicada en static a Base64.
    """

    image_path = finders.find(static_path)

    if not image_path:
        raise Exception(
            f"No se encontró la imagen: {static_path}"
        )

    with open(image_path, "rb") as image_file:
        return base64.b64encode(
            image_file.read()
        ).decode("utf-8")