from config import VKTOKEN, number_of_photo, YTOKEN
from yandex import YandexInterface
from VK_module import VKAPIClient
from GoogleDriveAPI import GoogleIntrface
from tqdm import tqdm
import json


if __name__ == '__main__':
    owner_id = input('Введите ID Пользователя "Вконтакте": ')
    from_vk_to_ya = input('Введите имя папки: ')
    choise = input('Какую платформу используем для бэкапа? \n'
                   'ЯндексДиск - введите "1" \n'
                   'GoogleDrive - введите  "2"\n'
                   'ЯндексДиск + GoogleDrive  - Введите "3"\n')
    yandex_interface = YandexInterface(YTOKEN)
    google_interface = GoogleIntrface()
    if choise == "1":
        yandex_interface.ya_create_folder(from_vk_to_ya)
    elif choise == '2':
        google_folder_id = google_interface.createFolder(from_vk_to_ya)
    elif choise == '3':
        yandex_interface.ya_create_folder(from_vk_to_ya)
        google_folder_id = google_interface.createFolder(from_vk_to_ya)
    else:
        print(f'{choise}  - Нет такого пункта в меню. Перезапустите программу и выберете из имеющихся')
        quit()
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
    max_photos = sorted(max_photos, reverse=True)[:number_of_photo]
    likes_array = []
    photos_log = []
    print(f'Загружаем {number_of_photo} фотографий ')
    pbar1 = tqdm(total=number_of_photo)
    for max_photo, size, likes, photo_url, date in max_photos:
        if likes in likes_array:
            likes = f'{likes}_{date}'
        current_file = {}
        likes_array.append(likes)
        current_file['file_name'] = f'{likes}.jpg'
        current_file['size'] = size
        if choise == "1":
            yandex_interface.ya_upload_photos(photo_url, likes)
        elif choise == '2':
            google_interface.gdrive_downloader(photo_url, likes, google_folder_id)
        elif choise == '3':
            yandex_interface.ya_upload_photos(photo_url, likes)
            google_interface.gdrive_downloader(photo_url, likes, google_folder_id)
        photos_log.append(current_file)
        pbar1.update(1)
    with open("photos_log.json", "w") as file:
        json.dump(photos_log, file, indent=4)
    print('Выполнено!')
