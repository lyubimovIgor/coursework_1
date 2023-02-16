# VKAPI.py
import requests
import json
from tqdm import tqdm
from YaUploader import YaUploader


class VKAPI:
    def __init__(self):
        self.token_VK = input('Введите токен приложения VK: ')
        self.user_ID = input('Введите ID пользователя VK: ')
        self.count_save = input('Введите порог выгрузки фото из VK (до 5 по умолчанию): ')
        if self.count_save.isdigit():
            self.count_save = int(self.count_save)
        else:
            self.count_save = 5
        self.ya = YaUploader()  # создание экземпляра класса YaUploader
        self.info = []  # список для хранения информации о загруженных файлах

    def start_parse(self):
        print(f'Старт выгрузки до: {self.count_save} фотографий')
        response = self.get_requests()
        if 'error' in response:
            print(f"Ошибка: Аккаунт ID:{self.user_ID} недоступен")
        elif response['response'].get('count', 0) == 0:
            print(f"Ошибка: На аккаунте ID:{self.user_ID} нет фотографий!")
        else:
            items = response['response']['items'][:self.count_save]
            for item in tqdm(items):
                file_name = f"{item['likes']['count']}.jpg"
                url = item['sizes'][-1]['url']
                print('Загрузка:', url)
                self.ya.get_foto(file_name, url)
                self.info.append({"file_name": file_name, "size": item['sizes'][-1]['type']})
            self.write_info_to_json()

    def get_requests(self):
        link = "https://api.vk.com/method/photos.get?"
        params = {
            'owner_id': self.user_ID,
            'album_id': 'profile',
            'extended': '1',
            'photo_sizes': '1',
            'access_token': self.token_VK,
            'v': '5.107'
        }
        response = requests.get(link, params=params)
        if response.status_code != 200:
            print('Неудача! Нет связи с сервером.')
        return response.json()

    def write_info_to_json(self):
        with open('info_foto_files.json', 'a') as f:
            json.dump(self.info, f, ensure_ascii=False, indent=2)



