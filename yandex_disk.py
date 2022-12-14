import datetime
import requests
from tqdm import tqdm


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def upload(self, vk_id, file_param):
        exist_files = []
        ya_token = self.token
        pbar = tqdm(total=len(file_param))
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {'Content-type': 'application/json',
                   'Accept': 'application/json',
                   'Authorization': f'OAuth {ya_token}'
                   }
        res = requests.get(f'{url}?path={vk_id}', headers=headers).json()
        try:
            if res['error'] == 'DiskNotFoundError':
                requests.put(f'{url}?path={vk_id}', headers=headers).json()
        except KeyError:
            for i in res['_embedded']['items']:
                exist_files.append(i['name'])
        for i in file_param:
            date = datetime.date.today()
            if f'{i["index"]}_{i["file_name"]}' not in exist_files:
                file_name = f'{i["index"]}_{i["file_name"]}'
            elif f'{i["index"]}_{i["file_name"].strip(".")[0]}_{date}.jpg' not in exist_files:
                file_name = f'{i["index"]}_{i["file_name"].strip(".")[0]}_{date}.jpg'
            else:
                print(f'Уже существуют файлы {i["index"]}_{i["file_name"]} и '
                      f'{i["index"]}_{i["file_name"].strip(".")[0]}_{date}.jpg в папке {vk_id}')
                continue
            res = requests.get(i['file_path'])
            response = requests.get(f'{url}/upload?path={vk_id}/{file_name}&overwrite=False',
                                    headers=headers).json()
            requests.put(response['href'], files={'file': res.content})
            pbar.update(1)
        pbar.close()
