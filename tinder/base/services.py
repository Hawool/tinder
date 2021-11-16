from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from matplotlib import pyplot as plt
from io import BytesIO
from math import radians, cos, sin, asin, sqrt


def get_path_upload_avatar(instance, file):
    """Построение пути к файлу, формат (media)/avatar/user_id/photo.png"""
    return f'avatar/{instance.id}/{file}'


def watermark(img):
    """Функция наносит водяной знак на изображение, в качестве знака и изображения используется одна и та же картинка,
    наносится она в верхний левый угол"""
    # to open the image
    image = Image.open(img)
    plt.imshow(image)

    # image watermark
    size = (500, 100)
    crop_image = image.copy()
    # to keep the aspect ration in intact
    crop_image.thumbnail(size)

    # add watermark
    copied_image = image.copy()
    # base image
    copied_image.paste(crop_image, (0, 0))
    # pasted the crop image onto the base image
    plt.imshow(copied_image)

    image_bytes = BytesIO()
    copied_image.save(image_bytes, format='png')
    new_image = InMemoryUploadedFile(
        image_bytes, None, img.name, 'image/png', None, None, None
    )
    return new_image


def km_distance(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers is 6371
    km = 6371 * c
    return km
