from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from matplotlib import pyplot as plt
from io import BytesIO


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
