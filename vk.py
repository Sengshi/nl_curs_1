import requests
import configparser
import json


def out_json(files):
    out = []
    for i in files:
        out.append({'file_name': i['file_name'], 'size': i['size']})
    with open('out2.json', 'w') as outfile:
        outfile.write(json.dumps(out, indent=4))


class VK:
    def __init__(self, vk_id):
        config = configparser.ConfigParser()
        config.read('settings.ini')
        self.params = {
            'access_token': config['VK']['token'],
            'v': '5.131',
        }
        self.id = vk_id
        self.url = 'https://api.vk.com/method'

    def get_vk_id(self):
        res = requests.get(f'{self.url}/users.get', params={**self.params,
                                                            'user_id': self.id}).json()['response'][0]['id']
        return res

    def get_albums(self):
        albums = {'profile': 'Photo profiles'}
        res_albums = requests.get(f'{self.url}/photos.getAlbums', params={**self.params, 'owner_id': self.get_vk_id()})
        for i in res_albums.json()['response']['items']:
            albums[str(i['id'])] = i['title']
        return albums

    def top_vk_photos(self, album, max_images=5):
        files = []
        album = album
        index = 0
        params_photo = {
            'album_id': album,
            'photo_sizes': 1,
            'extended': 1,
        }
        res_photo = requests.get(f'{self.url}/photos.get', params={
            **self.params,
            **params_photo,
            'owner_id': self.get_vk_id(),
        })
        for i in res_photo.json()['response']['items'][:-(int(max_images)+1):-1]:
            file = i['sizes'][len(i['sizes']) - 1]
            files.append({
                'index': index,
                'file_name': f'{i["likes"]["count"]}.jpg',
                'size': file['type'],
                'file_path': file['url'],
            })
            index += 1
        # json_file = json.dumps(files, indent=4)
        # with open('out.json', 'w', encoding='utf8') as json_out:
        #     json_out.write(json_file)
        out_json(files)
        return files
