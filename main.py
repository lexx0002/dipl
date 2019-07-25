from modules.vkauth import VKAuth
from modules.vkexec import VkExecute
from modules.db_mongo import DB_Mongo
from modules.vkapi import VkApi
from pprint import pprint
import json
import codecs

def adv_sort():
    crit_dict = {'com_group': 0, 'com_bdate': 0, 'com_interests': 0}
    crit_dict['com_group'] = input('Введите вес для критерия - Общие группы (от 1 до 3): ')
    crit_dict['com_bdate'] = input('Введите вес для критерия - Возраст (от 1 до 3): ')
    crit_dict['com_interests'] = input('Введите вес для критерия - Интересы (от 1 до 3): ')
    return crit_dict


def get_basic_partners(user_in, user_full_in):
    usr_full_var = user_full_in['response'][0]
    if 'city' not in user_full_in['response'][0]:
        usr_full_var['city'] = {'id': 0, 'title': ''}
        usr_full_var['city']['id'] = input('Введите код города по которому нужно проводить поиск: ')
    if 'bdate' not in user_full_in['response'][0]:
        usr_full_var['bdate'] = ''
        usr_full_var['bdate'] = input('Введите дату рождения в формате "D.M.YYYY": ')
    if len(user_full_in['response'][0]['bdate']) < 6:
        usr_full_var['bdate'] = ''
        usr_full_var['bdate'] = input('Введите дату рождения в формате "D.M.YYYY": ')
    partners_basic_out = user_in.get_partners_by_basic(usr_full_var['sex'], usr_full_var['city']['id'])['response']
    return partners_basic_out


def db_operation(db_in, partners_basic_in, user_full_in, user_in, user_id_in):
    for item in partners_basic_in['fr_list']:
        db_in.import_data(item)
    print('Формируем список потенциальных друзей для {}'.format(user_full_in['response']))
    db_in.put_fields()
    basic_id = db_in.get_basic_id()
    i = 0
    for id in basic_id:
        print('Обработка {} записи из {}'.format(i,len(basic_id)))
        if user_in.get_com_groups(user_id_in, id) > 1:
            db_in.put_value_com(id)
        i += 1
    max_age = input('Введите насколько лет партнер может быть старше ')
    min_age = input('Введите насколько лет партнер может быть младше ')
    db_in.put_value_bdate(user_full_in['response'][0]['bdate'], max_age, min_age)
    if 'interests' in user_full_in['response'][0].keys():
        for part in user_full_in['response'][0]['interests'].split():
            db_in.put_value_inter(part)


def list_to_json(list, path_f):
    with codecs.open(path_f, 'w', encoding='utf-8') as json_file:
        json.dump(list, json_file, ensure_ascii=False)


def main():
    get_auth = VKAuth(['friends'], '6889971', '5.95')
    get_auth.auth()
    print('Получен следующий токен {}'.format(get_auth._access_token))
    user_input = input('Введите id или имя пользователя: ')
    vkapi = VkApi(get_auth._access_token)
    user_id = vkapi.get_user_id(user_input)
    user_full = vkapi.get_user_inf(user_id)
    user = VkExecute(get_auth._access_token, user_id)
    db = DB_Mongo()
    db.all_drop()
    partners_basic = get_basic_partners(user, user_full)
    db_operation(db, partners_basic, user_full, user, user_id)
    adv_criteries = adv_sort()
    out_db = db.find_n_drop_adv(adv_criteries)
    out_list = []
    for item in out_db.find():
        x = vkapi.get_fr(item['id'])
        out_list.append(x)
    list_to_json(out_list, 'outjson.json')
    pprint(out_list)

if __name__ == "__main__":
    main()

