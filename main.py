import google_drive
import yandex_disk
from vk import VK


def main():
    while True:
        cloud = input('Куда выгрузить (google или yandex, q - для выхода): ')
        if cloud == 'q':
            print('Пока!!!')
            return
        elif cloud == 'google' or cloud == 'yandex':
            id_vk = input('Введите id пользователя VK: ')
            login = VK(id_vk)
            for i in login.get_albums():
                print(f'ID: {list(i.keys())[0]}, name: {list(i.values())[0]}')
            album = input('Album ID: ')
            max_photo = input('Ввдите количество фото (по умолчанию будет выгружаться 5): ')
            if not max_photo.isnumeric():
                print('Error')
                files = login.top_vk_photos(album)
            else:
                print('Excellent')
                files = login.top_vk_photos(album, max_photo)
            if cloud == 'yandex':
                token = input('Введите Ваш токен YandexDisk: ')
                ya_uploader = yandex_disk.YaUploader(token)
                ya_uploader.upload(id_vk, files)
            elif cloud == 'google':
                secret_file = input('Введите имя файла для Google API OATH2: ')
                google_uploader = google_drive.GoogleUploader(secret_file)
                google_uploader.upload(id_vk, files)
        else:
            print('Введите доступные команды!')
            continue


if __name__ == "__main__":
    main()
