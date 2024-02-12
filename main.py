from config import VKTOKEN, YTOKEN, choise
from yandex import YandexInterface
from VK_module import VKAPIClient
from GoogleDriveAPI import GoogleIntrface
from tqdm import tqdm
import json


def main():
    owner_id = input('Введите ID Пользователя "Вконтакте": ')
    from_vk_to_ya = f'{owner_id}_backup'
    yandex_interface = YandexInterface(YTOKEN)
    google_interface = GoogleIntrface()
    if choise == "1":
        yandex_interface.ya_create_folder(from_vk_to_ya)
    elif choise == '2':
        google_folder_id = google_interface.createFolder(from_vk_to_ya)
    elif choise == '3':
        yandex_interface.ya_create_folder(from_vk_to_ya)
        google_folder_id = google_interface.createFolder(from_vk_to_ya)
    max_photos, number_of_photo = VKAPIClient(VKTOKEN, owner_id).photo_sort()
    max_photos = sorted(max_photos, reverse=True)[:number_of_photo]
    likes_array = []
    photos_log = []
    print(f'Загружаем {number_of_photo} фотографии(й) ')
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


if __name__ == '__main__':
    main()
