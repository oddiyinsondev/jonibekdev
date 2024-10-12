import sqlite3
from config import BAZA

def insert_user(full_name,telegram_id,username,created_at):
    connection = sqlite3.connect(BAZA)
    cursor = connection.cursor()
    try:
        cursor.execute('INSERT INTO users (full_name,telegram_id,username,created_at) VALUES (?,?,?,?)', (full_name,telegram_id,username,created_at))
        # Сохраняем изменения и закрываем соединение
        connection.commit()
        connection.close()
    except:
        pass
    
def get_user():
    connection = sqlite3.connect(BAZA)
    cursor = connection.cursor()


    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    
    lst = []
    
    for user in users: 
        lst.append(user[2])
       
    return lst

def get_admin()-> list:
    connection = sqlite3.connect(BAZA)
    cursor = connection.cursor()


    cursor.execute('SELECT * FROM bot_admin')
    admins = cursor.fetchall()
    
    lst=[]
    

    
    for admin in admins:
        
            
        lst.append(admin[2])
    
    return lst


    
def insert_client(loyiha,full_name,username,phone_number,created_at):
    connection = sqlite3.connect(BAZA)
    cursor = connection.cursor()
    
    
    cursor.execute('INSERT INTO clients (loyiha,full_name,username,phone_number,created_at) VALUES (?,?,?,?,?)', (loyiha,full_name,username,phone_number,created_at))
    connection.commit()
    connection.close()
    
def insert_admin(full_name,telegram_id,username):
    connection = sqlite3.connect(BAZA)
    cursor = connection.cursor()
    
    
    cursor.execute('INSERT INTO bot_admin (full_name,telegram_id,username) VALUES (?,?,?)', (full_name,telegram_id,username))
    connection.commit()
    connection.close()
    

    
    
def get_all_clients() -> list:
    connection = sqlite3.connect(BAZA)
    cursor = connection.cursor()
    
    cursor.execute('SELECT * FROM clients')
    clients = cursor.fetchall()
    
    lst = []
    
    for client in clients:
        # print(client[1])
        lst.append(client)
    return lst
    


# for client in get_all_clients():
#     print(client[1])        


# print(get_all_clients())



# for client in get_all_clients():
#     print(client[3])