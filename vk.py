import requests
from config import vk_token


class VK:
    def __init__(self, vk_id):
        self.params = {
            'access_token': vk_token,
            'v': '5.131',
            'owner_id': vk_id,
        }
        self.url = 'https://api.vk.com/method'

    def get_albums(self):
        albums = {'profile': 'Photo profiles'}
        res_albums = requests.get(f'{self.url}/photos.getAlbums', params={**self.params})
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
        res_photo = requests.get(f'{self.url}/photos.get', params={**self.params, **params_photo})
        for i in res_photo.json()['response']['items'][:-(int(max_images)+1):-1]:
            file = i['sizes'][len(i['sizes']) - 1]
            files.append({
                'index': index,
                'file_name': f'{i["likes"]["count"]}.jpg',
                'size': file['type'],
                'file_path': file['url'],
            })
            index += 1
        return files
