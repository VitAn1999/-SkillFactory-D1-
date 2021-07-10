from config import auth_params
from config import board_id
import requests
import sys

base_url = 'https://api.trello.com/1/{}'

# Получаем полное id нашей доски
full_board_id = requests.get(base_url.format('boards') + '/' + board_id, params=auth_params).json()['id']


# Функция отображающая доску и поставленные задачи
def read():
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    for column in column_data:
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        print(column['name'], f'({len(task_data)}):')
        if not task_data:
            print('\t' + 'Нет задач')
            continue
        for task in task_data:
            print('\t' + task['name'])


# Функция создания новой задачи        
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


# Функция перемещения задачи в другие колонки
def move(name, column_name):
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    task_ids = {}
    task_id = None

    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name'] == name: 
                task_ids[task['id']] = column['name']
                continue
    if len(task_ids) == 1:
        for key in task_ids.keys():
            task_id = key
    else:
        task_id = check_task_name(name, task_ids)
            
    for index, column in enumerate(column_data):
        if column['name'] == column_name:
            put_card = requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})
            if put_card.status_code == requests.codes.ok:
                print(f'Задача {name} успешно перенесена в колонку {column_name}')
            else:
                put_card.raise_for_status()
            break
        elif index == len(column_data) - 1:
            print('Такой колонки не существует, проверьте правильность введенных данных')


# Функция создания новой колонки
def create_column(name):
    post_column = requests.post(base_url.format('lists'), {'name': name, 'idBoard': full_board_id, **auth_params})
    if post_column.status_code == requests.codes.ok:
        print(f'Колонка {name} успешно добавлена на доску')
    else:
        post_column.raise_for_status()


# Функция проверки имени задачи
def check_task_name(name, task_ids):
    print('\nНа доске есть несколько задач с одинаковым именем: ')

    for index, key in enumerate(task_ids.keys()):
        print(f'{index + 1}. Задача {name} c id {key} в колонке {task_ids[key]}')
    task_number = input('Укажите порядковый номер нужной: \n')

    for index, key in enumerate(task_ids.keys()):
        if str(index + 1) == task_number:
            return key
    print('Указан несуществующий номер. Повторите попытку.')
    return check_task_name(name, task_ids)


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
