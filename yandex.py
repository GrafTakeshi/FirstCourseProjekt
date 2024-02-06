import requests
from config import YTOKEN

url_yadisk = 'https://cloud-api.yandex.net'


def ya_create_folder(from_vk_to_ya):
    url_create_folder = f'{url_yadisk}/v1/disk/resources'
    params_yc = {
        'path': from_vk_to_ya
    }
    headers_y = {
        'Authorization': YTOKEN
    }
    response = requests.put(url_create_folder,
                            params=params_yc,
                            headers=headers_y)
    if 200 <= response.status_code < 300:
        print('Успешно создали Папку')
    elif response.status_code == 409:
        print('Такая папка уже существует')


def ya_upload_photos(from_vk_to_ya, photo_url, likes):
    url_yadisk_upload = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    params_yc = {
        'path': f'{from_vk_to_ya}/{likes}.jpg',
        'url': photo_url
    }
    headers_y = {
        'Authorization': YTOKEN
    }

    response = requests.post(url_yadisk_upload,
                             params=params_yc,
                             headers=headers_y
                             )
    if 200 <= response.status_code < 300:
        print(f'Успешно загрузили на диск Файл {likes}.jpg')
    else:
        print('Загрузка не удалась')

