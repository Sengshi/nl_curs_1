import os.path
import shutil
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from datetime import date, datetime


class GoogleUploader:
    def __init__(self, secret_file: str):
        self.secret_file = secret_file
        self.scope = 'https://www.googleapis.com/auth/drive'

    def upload(self, vk_id: str, file_param, dir_path='temp'):
        flow = InstalledAppFlow.from_client_secrets_file(self.secret_file, self.scope)
        creds = flow.run_local_server(port=8080)
        with open('log.txt', 'a', encoding='utf8') as logging:
            try:
                service = build('drive', 'v3', credentials=creds)
                results = service.files().list(
                    pageSize=100,
                    q=f'name = "{vk_id}" and mimeType = "application/vnd.google-apps.folder" '
                      f'and trashed != True').execute()
                items = results.get('files', [])
                if not items:
                    folder_metadata = {
                        'name': vk_id,
                        'mimeType': 'application/vnd.google-apps.folder'
                    }
                    folder = service.files().create(body=folder_metadata, fields='id'
                                                    ).execute()
                    folder_id = folder.get('id')
                else:
                    folder_id = items[0]['id']
                results = service.files().list(
                    pageSize=20,
                    fields="nextPageToken, files(id, name, mimeType, parents, createdTime)",
                    q=f'"{folder_id}" in parents').execute()
                exist_files = []
                for i in results['files']:
                    exist_files.append(i['name'])
                if not os.path.exists(dir_path):
                    os.mkdir(dir_path)
                for file_name in file_param:
                    temp = f'{file_name["index"]}_{file_name["file_name"]}'
                    with open(os.path.join(dir_path, temp), 'wb') as temp_file:
                        temp_file.write(requests.get(file_name['file_path']).content)
                    if temp not in exist_files:
                        name = temp
                    else:
                        param = file_name['file_name'].split('.')
                        name = f'{file_name["index"]}_{param[0]}_{date.today().strftime("%d-%m-%Y")}.{param[1]}'
                    if name not in exist_files:
                        file_metadata = {
                            'name': name,
                            'parents': [folder_id],
                        }
                        media = MediaFileUpload(os.path.join(dir_path, temp), mimetype='image/jpeg')
                        service.files().create(body=file_metadata,
                                               media_body=media,
                                               fields='id').execute()
                        logging.write(f'{datetime} {name} Upload Complete!')
                        print(f'{name} Upload Complete!')
                    else:
                        logging.write(f'{datetime} Уже существуют файлы в папке {vk_id}')
                        print(f'Уже существуют файлы в папке {vk_id}')
                        continue
                shutil.rmtree(dir_path)
            except HttpError as error:
                logging.write(f'{datetime} An error occurred: {error}')
                print(f'An error occurred: {error}')
