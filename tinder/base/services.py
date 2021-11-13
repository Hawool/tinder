def get_path_upload_avatar(instance, file):
    """Построение пути к файлу, формат (media)/avatar/user_id/photo.png"""
    return f'avatar/{instance.id}/{file}'