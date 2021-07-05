from config import auth_params
from config import board_id
import requests
import sys

base_url = 'https://api.trello.com/1/{}'

# Получаем полное id нашей доски
full_board_id = requests.get(base_url.format('boards') + '/' + board_id, params=auth_params).json()['id']


def read():
    print(board_data)
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    for column in column_data:
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        print(column['name'], f'({len(task_data)}):')
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
            print('Такой колонки не существует, проверьте правильность введенных данных')


def move(name, column_name):
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    task_id = None

    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name'] == name:
                task_id = task['id']
                break
        if task_id:
            break

    for index, column in enumerate(column_data):
        if column['name'] == column_name:
            put_card = requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})
            if put_card.status_code == requests.codes.ok:
                print(f'Задача {name} успешно перенесена в {column_name}')
            else:
                put_card.raise_for_status()
            break
        elif index == len(column_data) - 1:
            print('Такой колонки не существует, проверьте правильность введенных данных')


def create_column(name):
    post_column = requests.post(base_url.format('lists'), {'name': name, 'idBoard': full_board_id, **auth_params})
    if post_column.status_code == requests.codes.ok:
        print(f'Колонка {name} успешно добавлена на доску')
    else:
        post_column.raise_for_status()


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'create_column':
        create_column(sys.argv[2])
    else:
        print('Проверьте правильность введенной команды')
