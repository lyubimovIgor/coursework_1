#YaUploader.py
import requests


class YaUploader:
    def __init__(self):
        self.token = input('Введите токен полигона Яндекс.Диска: ')
        self.yandex_folder = input('Введите имя яндекс-папки: ')
        self.get_new_folder()

    def get_new_folder(self):
        up_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {
            'Content-Type': 'application/json' ,
            'Authorization': f'OAuth {self.token}'
        }
        params = {
            'path': self.yandex_folder ,
            'overwrite': 'true'
        }
        response = requests.put(up_url , headers=headers , params=params)
        if response.status_code != 201:
            print(f'Папка с именем: {self.yandex_folder} уже существует!')
        else:
            print(f'Папка: {self.yandex_folder} создана на Yandex disk')

    def get_foto(self , file_name , url):
        file_path = self.yandex_folder + '/' + file_name
        self.upload_file_yd(file_path , url)

    def upload_file_yd(self , file_path , url):
        up_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = {
            'Content-Type': 'application/json' ,
            'Authorization': f'OAuth {self.token}'
        }
        params = {'url': url , 'path': file_path}
        response = requests.post(up_url , headers=headers , params=params)
        response.raise_for_status()
        if response.status_code == 202:
            print('Файл загружен на Яндекс Диск')
