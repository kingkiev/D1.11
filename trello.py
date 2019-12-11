import sys
import requests

# Данные авторизации в API Trello 
auth_params = {
	'key': '__________________',  # Свой trello key
	'token': '____________________________________________-',  # Свой trello token
}

# Адрес, на котором расположен API Trello, # Именно туда мы будем отправлять HTTP запросы.  
base_url = "https://api.trello.com/1/{}"  
board_id = "__________"     #Здесь нужно ввести короткий id доски с которой вы хотети работать

def read():      
    # Получим данные всех колонок на доске:      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
    
    # print(column_data)  
    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:      
    for column in column_data:      
        # Получим данные всех задач в колонке и перечислим все названия      
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()      
        if not task_data:
            print('\nКолонка: ' + column['name'])      
            print('\t' + 'Нет задач!')      
            continue     

        print('\nКолонка: ' + column['name'] +  '\nКоличество задач: ' + str(len(task_data)))
        for task in task_data:  
            print('\tid: ' + str(task['idShort']) + ' - ' + task['name'])  

def create():
    name = input("\nКакое имя новой задачи? ").capitalize().strip()

    # Получим данные всех колонок на доске 
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    
    print("\nВыберете колонку для этой задачи:\n")
    for column in column_data:
        print(column['name'])
    column_name = input("\nКолонка: ").capitalize()      
                     
    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна      
    for column in column_data:      
        if column['name'] == column_name:      
            # Создадим задачу с именем _name_ в найденной колонке      
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})     
            break
    print(f"\nСоздана новая задача: '{name}' в колонке '{column_name}'")
    read()


def move():  
    id_card = input("Введите id задачи: ").strip()
    # Получим данные всех колонок на доске    
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()    
    # Среди всех колонок нужно найти задачу по имени и получить её id    
    task_id = None    
    for column in column_data:    
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()    
        for task in column_tasks:    
            if task['idShort'] == int(id_card):    
                task_id = task['id']
                break    
        if task_id:    
            break  

    ex_column_name = ''.join([column['name'] for column in column_data if column['id'] == task['idList']])
    print(f"Вы выбрали задачу '{task['name']}' с 'id: {task['idShort']}' из колонки '{ex_column_name}' ")     
    print('\nВ какую колонку вы хотите её перенести?\n')
    for column in column_data:
        print(column['name'])
    column_name = input("\nПеренос в колонку: ").capitalize().strip() 
    # Теперь, когда у нас есть id задачи, которую мы хотим переместить    
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу    
    for column in column_data:    
        if column['name'] == column_name:    
            # И выполним запрос к API для перемещения задачи в нужную колонку    
            requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})    
            break
    print(f"Задача '{task['name']}' с 'id: {task['idShort']}' перенесена в колонку '{column_name}' ")
    read()

def add_list():  
    name = input('ВВедите название для новой колонки: ').capitalize().strip()        
    # Получим данные всех колонок на доске   
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()    
   
    for column in column_data:
        id_board = column['idBoard']
        requests.post(base_url.format('lists'), data={'name': name, 'idBoard': id_board, 'pos': 'bottom',  **auth_params})    
        break
    print(f"\nНовая колонка с названием '{name}' создана")
    read()

if __name__ == "__main__":      
    read()
    print("\nЧто вы хотите сделать? ")
    while True:
        act = input("\nВВедите действие: создать колонку - нажмите 1  или перейти к задачам - нажмите 2: ").strip()
        if act == "1":
            add_list()
            break
        elif act == "2":
            print('\nВы хотите создать новую задачу или переместить существующую?')

            while True:
                act_with_task = input("\nВведите: создать - нажмите 1, либо переместить - нажмите 2: ").strip()
                if act_with_task == "1":
                    create()
                    break
                elif act_with_task == "2":
                    move()
                    break
                else:
                    print('\nВведено некорректное действие')
            break
        elif act == 'q':
            break
        else:
            print('\nВведено некорректное действие')