import google_drive
import yandex_disk
import vk


def main():
    while True:
        cloud = input('Куда выгрузить (google или yandex, q - для выхода): ')
        if cloud == 'q':
            print('Пока!!!')
            return
        elif cloud == 'google' or cloud == 'yandex':
            id_vk = input('Введите id пользователя VK: ')
            files = vk.top_vk_photos(id_vk)
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
