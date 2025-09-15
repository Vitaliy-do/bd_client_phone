

import psycopg2


'''1. Функция создание базы данных'''
def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS client (id SERIAL PRIMARY KEY, name VARCHAR (90), lastname VARCHAR (90), email VARCHAR (90), phone VARCHAR (90));")
        cur.execute("CREATE TABLE IF NOT EXISTS phone (id_phone SERIAL PRIMARY KEY, phone VARCHAR(90), id_client INTEGER REFERENCES client(id));")
    conn.commit()
    print("Таблицы созданы")


'''2. Функция добавления клиентов в базу данных'''
def add_client(conn, name, lastname, email, phone=None):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO client(name, lastname, email) VALUES(%s, %s, %s) RETURNING id;", (name, lastname, email))
        id_client = cur.fetchone()[0]
        if phone is not None:
            cur.execute("INSERT INTO phone(phone, id_client) VALUES (%s, %s);", (phone, id_client))
    conn.commit()
    print(f"Клиент {name} {lastname} добавлен")


'''3. Функция добавления телефона клиента в базу данных'''
def add_phone(conn, id_client, phone):
    with conn.execute() as cur:
        cur.execute("INSERT INTO phone(phone, client_id) VALUES (%s, %s);", (phone, id_client))
    conn.commit()
    print(f"Телефон {phone} добавлен клиенту {id_client}")    


'''4. Функция изменения данных о клиенте в базе данных'''
def change_client(conn, id_client, name=None, lastname=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute("UPDATE client SET name = %s, lastname = %s, email = %s WHERE id = %s);", (name, lastname, email, id_client))
        if phone is not None:
            cur.execute("INSERT INTO phone(phone, id_client) VALUES (%s, %s);", (phone, id_client))
    conn.commit()
    print(f"Клиент добавлен")


'''5. Функция удаления номера телефорна клиента из базы данных'''
def delete_phone(conn, id_client, phone):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM phone WHERE id_client = %s AND phone = %s;" (id_client, phone))
    conn.commit()
    print(f"Телефон {phone} удален клиента {id_client}")


'''6. Функция удаления клиента из базы данных'''
def delete_client(conn, id_client):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM phone WHERE id_client = %s;" (id_client,))
        cur.execute("DELETE FROM client WHERE id = %s; (id_client,)")

    conn.commit()
    print(f"Клиент с  id = {id_client} удален")


'''7. Функция поиска клиента с использованием его данных из базы данных'''
def find_client(conn, name=None, lastname=None, email=None, phone=None):
    with conn.cursor() as cur:
        if name:
            cur.execute("SELECT * FROM client WHERE name = %s;" (name))
            return cur.fetchall()
        if lastname:
            cur.execute("SELECT * FROM client WHERE lastname = %s;" (lastname))
            return cur.fetchall()
        if email:
            cur.execute("SELECT * FROM client WHERE email like %s" ("%" + email + "%"))
            return cur.fetchall()
        if phone:
            cur.execute("SELECT * FROM client WHERE phone like %s" ("%" + phone + "%"))
            return cur.fetchall()


if __name__== '__man__':
    with psycopg2.connect(ddatabase = "test5", 
                          user = "postgres",
                          password = "P@ssw0rd5") as conn:
       with conn.cursor() as cur:
    
       # 1.Создание базы данных
        create_db(conn) 

       # 2.Добавление клентов в базу даных
        client1 = add_client(conn, "Лев", "Толстой", "lev_t@ya.ru", "+79995557744")
        client2 = add_client(conn, "Сергей", "Есенин", "serg_e@ya.ru", "+79995557788")
        client3 = add_client(conn, "Александр", "Пушкин", "alex_p@ya.ru")

       # 3.Добавление телефона клиента в базу данных
        add_phone(conn, client3, "+79995554444")

       # 4.Изменение данных о клиенте в базе данных
        change_client(conn, client1, "levon_tolstoy@ya.ru")

       # 5.Удаление номера телефорна клиента из базы данных
        delete_phone(conn, client2, "+79995554444")

       # 6.Удаление клиента из базы данных
        delete_client(conn, client1)

       # 7.Поиск клиента с использованием его данных из базы данных
       # 7.1 Поиск клиента по имени
        find_client(conn, name= "Лев", lastname=None, email=None, phone=None)
       # 7.2 Поиск клиента по фамилии
        find_client(conn, name= None, lastname= "Толстой", email=None, phone=None)
       # 7.3 Поиск клиента по электронной почте
        find_client(conn, name= None, lastname= None, email= "alex_p@ya.ru", phone=None)
       # 7.3 Поиск клиента по телефону
        find_client(conn, name=None, lastname=None, email=None, phone= "+79995557744")


       conn.close()
