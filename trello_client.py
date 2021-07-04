from config import auth_params
from config import board_id
import requests
import sys

base_url = 'https://api.trello.com/1/{}'


def read():
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    for column in column_data:
        print(column['name'])
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        if not task_data:
            print('\t' + 'Нет задач')
            continue
        for task in task_data:
            print('\t' + task['name'])

        
def create(name, column_name):
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    for index, column in enumerate(column_data):
        if column['name'] == column_name:
            post_card = requests.post(base_url.format('cards'), {'name': name, 'idList': column['id'], **auth_params})
            if post_card.status_code == requests.codes.ok:
                print(f'Задача {name} успешно добавлена в {column_name}')
            else:
                post_card.raise_for_status()
            break
        elif index == len(column_data) - 1:
            print(len('Такой колонки не существует, проверьте правильность введенных данных'))


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    else:
        print('Проверьте правильность введенной команды')
