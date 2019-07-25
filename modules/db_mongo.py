import re
from pymongo import MongoClient


class DB_Mongo:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client.hmwrk_db

    def import_data(self, list_in):
        data = self.db.buf3
        data.insert_one(list_in).inserted_id

    def drop(self):
        self.db.data.drop()

    def item_count(self):
        return(self.db.data.find().count())

    def find_n_drop_adv(self, adv_criteries_in):
        crit_list = ['com_group', 'com_bdate', 'com_interests']

        find_buf_3 = self.db.buf3
        find_buf_4 = self.db.buf4
        find_buf_5 = self.db.buf5
        find_buf_6 = self.db.buf6

        for crit in crit_list:
            if adv_criteries_in.get(crit) == '1':
                for item in self.db.buf3.find({crit: 1}):
                    find_buf_4.insert_one(item).inserted_id
                if self.db.buf4.find().count() < 10:
                    i = 0
                    for item in self.db.buf3.find({crit: 0}):
                        find_buf_4.insert_one(item).inserted_id
                        i +=1
                        if i == 10:
                            break
        self.db.buf3.drop()

        for crit in crit_list:
            if adv_criteries_in.get(crit) == '2':
                for item in self.db.buf4.find({crit: 1}):
                    find_buf_5.insert_one(item).inserted_id
                if self.db.buf5.find().count() < 10:
                    i = 0
                    for item in self.db.buf4.find({crit: 0}):
                        find_buf_5.insert_one(item).inserted_id
                        i += 1
                        if i == 10:
                            break
        self.db.buf4.drop()

        for crit in crit_list:
            if adv_criteries_in.get(crit) == '3':
                for item in self.db.buf5.find({crit: 1}):
                    find_buf_6.insert_one(item).inserted_id
                if self.db.buf6.find().count() < 10:
                    i = 0
                    for item in self.db.buf5.find({crit: 0}):
                        find_buf_6.insert_one(item).inserted_id
                        i += 1
                        if i == 10:
                            break
        self.db.buf5.drop()
        print('Найдено {} потенциальных друзей'.format(self.db.buf6.find().count()))
        return self.db.buf6

    def put_fields(self):
        self.db.buf3.update({},
                          {'$set':{'com_group':0}},
                          multi=True)
        self.db.buf3.update({},
                            {'$set': {'com_bdate': 0}},
                            multi=True)
        self.db.buf3.update({},
                            {'$set': {'com_interests': 0}},
                            multi=True)

    def put_value_com(self, id_in):
        self.db.buf3.update({'id': id_in},
                            {'$set': {'com_group': 1}}, multi=True)

    def put_value_bdate(self, bdate_in, max_in, min_in):
        for item in self.db.buf3.find():
            if (item.get('bdate') is not None) and (len(item.get('bdate')) > 6) and (len(bdate_in) > 6):
                if int(item['bdate'][-4:]) in range(int(bdate_in[-4:]) - int(min_in), int(bdate_in[-4:]) + int(max_in)):
                    self.db.buf3.update({'id': item['id']},
                                        {'$set': {'com_bdate': 1}}, multi=True)

    def put_value_inter(self, inter_in):
        regex = re.compile('.*' + inter_in + '.*')
        for item in self.db.buf3.find({'interests': regex}):
            self.db.buf3.update({'id': item['id']},
                                {'$set': {'com_interests': 1}}, multi=True)

    def get_basic_id(self):
        id_list = []
        for item in self.db.buf3.find():
            id_list.append(item['id'])
        return id_list

    def print_n_drop_db(self):
        for item in self.db.buf6.find():
            print(item)
        self.db.buf6.drop()

    def print_basic_list(self):
        for item in self.db.buf3.find():
            print(item)

    def all_drop(self):
        self.db.buf3.drop()
        self.db.buf4.drop()
        self.db.buf5.drop()
        self.db.buf6.drop()

