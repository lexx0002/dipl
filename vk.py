from collections import Counter
import time
from urllib.parse import urlencode
import requests
from db.mysql import MySQLdb
from random import randint

class User:

    def __init__(self, id, info, weight=0):

        self.id = id
        self.info = info
        self.weight = weight

class Vkinder(MySQLdb):
    version = '5.101'
    app_id = '' # тут я использовал левый что нашел, с прошлого диплома не работает. Поэтому оставляю это поле для вас
    def __init__(self, main_user_id):
        app_id = input('Введите действительный APP_ID, так как прошлый наш не работает. ')
        url = 'https://oauth.vk.com/authorize'
        auth_data = {
            'client_id': app_id,
            'display': 'page',
            'response_type': 'token',
            'scope': 'status.friends',
            'v': self.version
        }
        print('?'.join((url, urlencode(auth_data))))
        self.token = input('Введите полученный токен: ')
        response_main_user = requests.get('https://api.vk.com/method/users.get', {
            'access_token': self.token,
            'user_ids': main_user_id,
            'fields': 'bdate, sex, interests, music, books, city',
            'v': self.version
        })

        main_user_info = response_main_user.json()['response'][0]
        self.main_user = User(main_user_info.pop('id'), main_user_info)

    def find_users(self, min_age, max_age):
        sex_for_find = 0
        if self.main_user.info['sex'] == 1:
            sex_for_find = 2
        else:
            sex_for_find = 1

        params = {
            'access_token': self.token,
            'sex': sex_for_find,
            'age_from': min_age,
            'age_to': max_age,
            'has_photo': 1,
            'fields': 'interests, music, books, sex, city',
            'count': 1000,
            'city': self.main_user.info['city']['id'],
            'v': self.version
        }

        response_find_users = requests.get('https://api.vk.com/method/users.search', params)
        users = []
        for user in response_find_users.json()['response']['items']:
            users.append(User(user.pop('id'), user))
        return users

    def count_weight(self, users, field='interests', multiplier=1):
        if self.main_user.info[field] != '':
            splitted_main_user_interests = self.main_user.info[field].split(',')
            for user in users:
                counter = 0
                if field in user.info:
                    splitted_interests = user.info[field].split(',')
                    word_counter = Counter(splitted_interests)
                    for interest in splitted_main_user_interests:
                        counter += word_counter[interest]
                user.weight += counter * multiplier
        return users

    def sort_users(self, finded_users):
        self.count_weight(finded_users, 'interests', 3)
        self.count_weight(finded_users, 'music', 2)
        self.count_weight(finded_users, 'books', 1)

        finded_users.sort(key=lambda user: user.weight, reverse=True)
        old_users = self.select_from_db([self.main_user.id])
        try:
            old_users[0]
            for old_user in old_users[0]['finded_users']:
                for user in finded_users:
                    if user.id == old_user or user.info['is_closed']:
                        finded_users.remove(user)
        except IndexError:
            for user in finded_users:
                if user.info['is_closed']:
                    finded_users.remove(user)

        return finded_users[0:10]

    def insert_db(self, final):
        for user in final:
            for photo in user.get('photos'):
                self.insert_to_db([user['id'], photo['id'], photo['likes']])

    def find_and_sort_photos(self, finded_users):
        sorted_users = []
        for user in finded_users:
            params = {
                'access_token': self.token,
                'owner_id': user.id,
                'extended': 1,
                'album_id': 'profile',
                'v': self.version
            }
            get_photos = requests.get('https://api.vk.com/method/photos.get', params)
            unsorted_photos = {
                'id': user.id,
                'photos': get_photos.json()['response']['items']
            }
            unsorted_ids_of_photos = []
            for photo in unsorted_photos['photos']:
                unsorted_ids_of_photos.append({
                    'id': photo['id'],
                    'likes': photo['likes']['count']
                })
            unsorted_ids_of_photos.sort(key=lambda dict: dict['likes'], reverse=True)
            unsorted_ids_of_photos = unsorted_ids_of_photos[0:2]
            sorted_users.append({
                'id': unsorted_photos['id'],
                'photos': unsorted_ids_of_photos
            })
            time.sleep(0.3)
            print(randint(1, 9)) # просто числа чтобы показывало что работает
        return sorted_users
