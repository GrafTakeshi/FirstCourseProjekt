from config import VKTOKEN, number_of_photo
from yandex import ya_create_folder, ya_upload_photos
from VK_module import VKAPIClient
import json


if __name__ == '__main__':
    owner_id = input('Введите ID Пользователя "Вконтакте": ')
    from_vk_to_ya = input('Введите имя папки: ')
    ya_create_folder(from_vk_to_ya)
    vk = VKAPIClient(VKTOKEN, owner_id).get_photo()
    photos_count = vk['response']['count']
    if photos_count < number_of_photo:
        print(f'В запрашеваемом профиле меется только {photos_count} фото! Скачаем их')
        number_of_photo = photos_count
    max_photos = []
    for photo in vk['response']['items']:
        max_size = ''
        photo_url = ''
        likes = ''
        max_photo = 0
        current_photo = []
        date = photo['date']
        for size in photo['sizes']:
            if size['type'] > max_size:
                likes = str(photo['likes']['count'])
                max_size = size['type']
                photo_url = size['url']
                max_photo = size['height'] * size['width']
        current_photo.append(max_photo)
        current_photo.append(max_size)
        current_photo.append(likes)
        current_photo.append(photo_url)
        current_photo.append(date)
        max_photos.append(current_photo)
    max_photos = sorted(max_photos, reverse=True)[:photos_count]
    likes_array = []
    photos_log = []
    for max_photo, size, likes, photo_url, date in max_photos:
        if likes in likes_array:
            likes = f'{likes}_{date}'
        current_file = {}
        likes_array.append(likes)
        current_file['file_name'] = f'{likes}.jpg'
        current_file['size'] = size
        ya_upload_photos(from_vk_to_ya, photo_url, likes)
        photos_log.append(current_file)
    with open("photos_log.json", "w") as file:
        json.dump(photos_log, file, indent=4)
