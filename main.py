import pprint
from vk import Vkinder

if __name__ == '__main__':
    user = input('ID пользователя:')
    ages = input('Введите диапазон возрастов через пробел: ').split(' ')
    vkinder = Vkinder(user)
    finded_users = vkinder.find_users(ages[0], ages[1])
    sorted_users = vkinder.sort_users(finded_users)
    final_users = vkinder.find_and_sort_photos(sorted_users)
    vkinder.insert_db(final_users)
    print()
    pprint.pprint(final_users)

