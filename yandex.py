import requests


class YandexInterface:
    url_yadisk = 'https://cloud-api.yandex.net'

    def __init__(self, YTOKEN):
        self.katalog = None
        self.token = YTOKEN

    def ya_create_folder(self, katalog):
        self.katalog = katalog
        url_create_folder = f'{self.url_yadisk}/v1/disk/resources'
        params_yc = {
            'path': self.katalog
        }
        headers_y = {
            'Authorization': self.token
        }
        response = requests.put(url_create_folder,
                                params=params_yc,
                                headers=headers_y)
        if 200 <= response.status_code < 300:
            print('Успешно создали Папку')
        elif response.status_code == 409:
            print('Такая папка уже существует')

    def ya_upload_photos(self, photo_url, likes):
        url_yadisk_upload = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params_yc = {
            'path': f'{self.katalog}/{likes}.jpg',
            'url': photo_url
        }
        headers_y = {
            'Authorization': self.token
        }

        response = requests.post(url_yadisk_upload,
                                 params=params_yc,
                                 headers=headers_y
                                 )
        if 200 <= response.status_code < 300:
            print(f'Успешно загрузили на диск Файл {likes}.jpg')
        else:
            print('Загрузка не удалась')
