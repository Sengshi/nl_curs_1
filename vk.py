import requests


def create_json(file_name, size, file_path):
    json_data = {
        'file_name': file_name,
        'size': size,
        'file_path': file_path,
    }
    return json_data


def top_vk_photos(vk_id: str, max_images=5):
    files = []
    album = 'profile'
    vk_token = 'vk1.a.3PUEDymMQ9XJziADuP1AapWqsWa1c1AARVGtumN5CgV8LW6hlWPpCKRLKuhdDduu9fSVLXfAhZSM_' \
               'pUi98rVQvTJYvQPNqQ3TiRjU4oBTgsbk1fB75CR8_dfm27bp2WGxlaN7prnCRTxYtzygeLNDo4PYMGeqc6b' \
               'puPAduIElw9u49RUeKC_FMa1TgWUi0nK'
    version = '5.131'
    url = 'https://api.vk.com/method'
    params = {'access_token': vk_token,
              'v': version,
              'users_id': vk_id,
              'album_id': album,
              'photo_sizes': 1
              }
    response = requests.get(f'{url}/photos.get', params={**params, 'extended': 1})
    for i in response.json()['response']['items'][:-(max_images+1):-1]:
        file = i['sizes'][len(i['sizes']) - 1]
        file_name = f'{i["likes"]["count"]}.jpg'
        size = file['type']
        file_path = file['url']
        files.append(create_json(file_name, size, file_path))
    return files
