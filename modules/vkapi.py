import requests

class VkApi:
    def __init__(self, token):
        self.token = token

    def get_user_id(self, usr_in):
        try:
            int(usr_in)
            return int(usr_in)
        except ValueError:
            params = {
                'user_ids': usr_in,
                'access_token': self.token,
                'v': 5.92,
                'fields': 'sex, bdate, city, interests, relation'
            }
            try:
                response_get_id = requests.get(
                    'https://api.vk.com/method/users.get',
                    params
                )
                return int(response_get_id.json()['response'][0]['id'])
            except Exception as e:
                print(response_get_id.json()['error']['error_msg'])

    def get_user_inf(self, id_in):
        params = {
            'user_ids': id_in,
            'access_token': self.token,
            'v': 5.92,
            'fields': 'sex, bdate, city, interests, relation'
        }
        try:
            response_get_usr = requests.get(
                'https://api.vk.com/method/users.get',
                params
            )
            return response_get_usr.json()
        except Exception as e:
            print(response_get_usr.json()['error']['error_msg'])

    def get_fr(self, id):
        params = {
            'owner_id': id,
            'access_token': self.token,
            'v': 5.95,
            'extended': '1',
            'album_id': 'profile'
        }
        try:
            response_fr_json = requests.get(
                'https://api.vk.com/method/photos.get',
                params
            )
        except Exception as e:
            print(response_fr_json.json()['error']['error_msg'])

        if 'error' not in response_fr_json.json():
            url_photos = []
            flag = 0
            photos = response_fr_json.json()['response']['items']
            photos = sorted(photos, key=lambda k: k['likes']['count'])
            photos = photos[-3:]
            for item in photos:
                flag = 0
                for size in item['sizes']:
                    if size['type'] == 'o':
                        url_photos.append(size['url'])
                        flag = 1
                if flag == 0:
                    url_photos.append(item['sizes'][0]['url'])
            fr_out = {'usr_url': 'https://vk.com/id' + str(photos[0]['owner_id']), 'top3_photos': url_photos}
        else:
            fr_out = {'usr_url': 'https://vk.com/id' + str(id), 'top3_photos':'private profile'}
        return fr_out
