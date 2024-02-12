import requests
from config import number_of_photo


# https://api.vk.com/method/status.get?<PARAMS>
class VKAPIClient:
    API_BASE_URL = 'https://api.vk.com/method'

    def __init__(self, token, owner_id):
        self.token = token
        self.owner_id = owner_id
        self.number_of_photo = number_of_photo

    def get_comon_params(self):
        return {
            'access_token': self.token,
            'owner_id': self.owner_id,
            'album_id': 'profile',
            'extended': True,
            'v': '5.131'
        }

    def get_photo(self):
        params = self.get_comon_params()
        response = requests.get(f'{self.API_BASE_URL}/photos.get', params=params)
        return response.json()
    def get_all(self):
        params = self.get_comon_params()
        params.update({
            'owner_id': self.owner_id,
            'album_id': ''

        })
        response = requests.get(f'{self.API_BASE_URL}/photos.getAll', params=params)
        return response.json()
    def photo_sort(self):
        self.vk = self.get_photo()
        photos_count = self.vk['response']['count']
        if photos_count < self.number_of_photo:
            print(f'В запрашеваемом профиле меется только {photos_count} фото! Скачаем их')
            self.number_of_photo = photos_count
        max_photos = []
        for photo in self.vk['response']['items']:
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
        return max_photos, self.number_of_photo




