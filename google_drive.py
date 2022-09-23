import json
import os.path
import shutil
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from datetime import date


class GoogleUploader:
    def __init__(self, secret_file: str):
        self.secret_file = secret_file
        self.scope = 'https://www.googleapis.com/auth/drive'

    def upload(self, vk_id: str, file_param, dir_path='temp'):
        flow = InstalledAppFlow.from_client_secrets_file(self.secret_file, self.scope)
        creds = flow.run_local_server(port=8080)
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
            for i in file_param:
                with open(os.path.join(dir_path, i['file_name']), 'wb') as temp_file:
                    temp_file.write(requests.get(i['file_path']).content)
                with open(os.path.join(dir_path, f'temp.json'), 'w', encoding='utf8') as temp:
                    json.dump(file_param, temp, indent=3)
            for file_name in file_param:
                if file_name['file_name'] not in exist_files:
                    name = file_name['file_name']
                else:
                    param = file_name['file_name'].split('.')
                    name = f'{param[0]}_{date.today().strftime("%d-%m-%Y")}.{param[1]}'
                if name not in exist_files:
                    file_metadata = {
                        'name': name,
                        'parents': [folder_id],
                    }
                    media = MediaFileUpload(os.path.join(dir_path, file_name['file_name']), mimetype='image/jpeg')
                    service.files().create(body=file_metadata,
                                           media_body=media,
                                           fields='id').execute()
                    print(f'{name} Upload Complete!')
                else:
                    print(f'Уже существуют файлы {file_name["file_name"]} и {name} в папке {vk_id}')
                    continue
            shutil.rmtree(dir_path)
        except HttpError as error:
            print(f'An error occurred: {error}')
