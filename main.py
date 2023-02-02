import requests
import json


class YaUploader:
    def __init__(self):
        self.token_VK = input('Введите токен приложения VK: ')
        self.token = input('Введите токен полигона Яндекс.Диска: ')
        self.user_ID = input('Введите ID пользователя VK: ')
        self.yandex_folder = input('Введите имя яндекс-папки: ')
        self.coint_save = input('Введите порог выгрузки фото из VK (до 5 по умолчанию): ')
        self.get_new_folder()


    def start_parse(self):
        if self.coint_save.isdigit():
            self.coint_save = int(self.coint_save)
            print(f'Старт выгрузки до: {self.coint_save} фотографий')
            self.parse_response()
        else:
            self.coint_save = 5
            print(f'Старт выгрузки до: {self.coint_save} фотографий')
            self.parse_response()


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


    def parse_response(self):
        count = 0
        if 'error' in self.get_requests():
            print(f'Ошибка: Аккаунт ID:{self.user_ID} недоступен')
        elif self.get_requests()['response'].get('count', False) == 0:
            print (f'Ошибка: На аккаунте ID:{self.user_ID} нет фотографий!')
        else:
            # print(self.get_requests()['response'].get('count', False))
            for i in self.get_requests()['response']['items']:
                if count < self.coint_save:
                    info = []
                    prep_dict = dict([('file_name', str(i['likes']['count']) + '.jpg'), ('size', i['sizes'][-1]['type'])])
                    print('Загрузка:', i['sizes'][-1]['url'])
                    self.get_foto(str(i['likes']['count']) + '.jpg', i['sizes'][-1]['url'])
                    info.append(prep_dict)
                    self.writer_json(info)
                    count += 1


    def get_foto(self, file_name, url):
        file_path = self.yandex_folder + '/' + file_name
        self.upload_file_yd(file_path, url)


    def writer_json(self, info):
        with open('info_foto_files.json', 'a') as f:
            json.dump(info, f, ensure_ascii=False, indent=2)


    def get_new_folder(self):
        up_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }
        params = {
            'path': self.yandex_folder,
            'overwrite': 'true'
        }
        response = requests.put(up_url, headers=headers, params=params)
        if response.status_code != 201:
            print(f'Папка с именем: {self.yandex_folder} уже существует!')
        else:
            print(f'Папка: {self.yandex_folder} создана на Yandex disc')


    def upload_file_yd(self, file_path: str, url):
        up_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = {'Content-Type': 'application/json', 'Authorization': 'OAuth {}'.format(self.token)}
        params = {'url': url, 'path': file_path}
        response = requests.post(up_url, headers=headers, params=params)
        response.raise_for_status()
        if response.status_code == 202:
            print('Файл загружен на Яндекс Диск')


if __name__ == '__main__':

    uploader = YaUploader()
    uploader.start_parse()





