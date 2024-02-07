import requests


# https://api.vk.com/method/status.get?<PARAMS>
class VKAPIClient:
    API_BASE_URL = 'https://api.vk.com/method'

    def __init__(self, token, owner_id):
        self.token = token
        self.owner_id = owner_id

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
