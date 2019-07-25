import time
import requests


class VkExecute:
    def __init__(self, token, id):
        self.token = token
        self.id = id

    def vk_request(self, params_in):
        response = requests.get(
            'https://api.vk.com/method/execute',
            params_in
        )
        time.sleep(0.33)
        out = response.json()
        return response.json()

    def check_resp(self, resp_in):
        if resp_in['response']['fr_groups'] != None:
            if resp_in['response']['usr_groups'] != None:
                return len(list(set(resp_in['response']['usr_groups']) & set(resp_in['response']['fr_groups'])))
            else:
                return 0
        else:
            return 0

    def get_partners_by_basic(self, usr_sex_in, usr_city_in):
        params = {'access_token': self.token, 'v': 5.95,
                  'code': ''
                          'var fr_sex = 0;'
                          'if (('+ str(usr_sex_in) +') == "1")'
                          '{'
                          'fr_sex = 2;} else {'
                          'fr_sex = 1; }'
                          'var fr_list = API.users.search({count: 200, '
                          'city:'+ str(usr_city_in) +', status: 6,'
                          'sex: fr_sex});'
                          'var fr_params = API.users.get({user_ids: fr_list.items@.id, '
                          'fields: "sex, bdate, city, interests, relation"});'               
                          'return {"fr_list":fr_params};'
                  }
        try:
            return self.vk_request(params)
        except requests.exceptions.ConnectionError:
            print('Ошибка соединения. Ждем 5 сек после чего попытается восстановить связь!')
            time.sleep(5)
            try:
                return self.vk_request(params)
            except requests.exceptions.ConnectionError:
                print('Ошибка соединения. Ждем 10 сек после чего попытается восстановить связь!')
                time.sleep(10)
                try:
                    return self.vk_request(params)
                except requests.exceptions.ConnectionError:
                    print('Ошибка соединения. Завершение работы Программы.')

    def get_com_groups(self, usr_id, fr_id):
        params = {'access_token': self.token, 'v': 5.95,
                  'code': ''
                          'var usr_groups =API.groups.get({user_id:' + str(usr_id) + '}).items;'  # группы User
                          'var fr_groups =API.groups.get({user_id:' + str(fr_id) + '}).items;'    # группы друга
                          'return {"usr_groups":usr_groups, "fr_groups":fr_groups};'
                  }
        try:
            req = self.vk_request(params)
            return self.check_resp(req)
        except requests.exceptions.ConnectionError:
            print('Ошибка соединения. Ждем 5 сек после чего попытается восстановить связь!')
            time.sleep(5)
            try:
                req = self.vk_request(params)
                return self.check_resp(req)
            except requests.exceptions.ConnectionError:
                print('Ошибка соединения. Ждем 10 сек после чего попытается восстановить связь!')
                time.sleep(10)
                try:
                    req = self.vk_request(params)
                    return self.check_resp(req)
                except requests.exceptions.ConnectionError:
                    print('Ошибка соединения. Завершение работы Программы.')

