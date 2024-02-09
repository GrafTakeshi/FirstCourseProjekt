from pydrive.auth import GoogleAuth
import io
import json
import requests




class GoogleIntrface:
    API_BASE_URL = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart"

    def __init__(self):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        self.token = gauth.attr['credentials'].access_token



    def gdrive_downloader(self, url, file_name, folder_id):
        self.url = url
        self.filename = file_name
        self.folder_id = folder_id
        self.metadata = {
            "name": self.filename,
            "parents": [self.folder_id]
        }
        self.files = {
            'data': ('metadata', json.dumps(self.metadata), 'application/json'),
            'file': io.BytesIO(requests.get(url).content)
        }
        response = requests.post(
            self.API_BASE_URL,
            headers={"Authorization": "Bearer " + self.token},
            files=self.files
        )


    def createFolder(self, folderName):
        url = 'https://www.googleapis.com/drive/v3/files'
        headers = {
            "Authorization": "Bearer " + self.token,
            'Content-Type': 'application/json'
        }
        metadata = {
            'name': folderName,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        response = requests.post(url, headers=headers, data=json.dumps(metadata))

        return response.json().get('id')
