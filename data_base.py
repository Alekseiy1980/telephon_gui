import sqlite3
import json
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets

help_ = []


try:

    with open("help.json","r", encoding="utf-8") as h:
        help_ = json.load(h)
except:
    pass

# создание базы данных и таблицы контактов
conn = sqlite3.connect('phonebook.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS contacts
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              first_name TEXT NOT NULL,
              last_name TEXT NOT NULL,
              phone_number TEXT NOT NULL,
              email TEXT,
              category TEXT)''')
conn.commit()
tel = pd.read_sql("select * from contacts",conn)
# функция для добавления нового контакта
def add_contact(first_name, last_name, phone_number, email='', category=''):
    # проверка на уникальность номера телефона
    c.execute("SELECT * FROM contacts WHERE phone_number=?", (phone_number,))
    if c.fetchone():
        print('Контакт с таким номером телефона уже существует!')
    else:
        c.execute("INSERT INTO contacts (first_name, last_name, phone_number, email, category) VALUES (?, ?, ?, ?, ?)",
                  (first_name, last_name, phone_number, email, category))
        conn.commit()
        print('Контакт успешно добавлен!')



# функция для поиска контактов
def search_contacts(query):
    c.execute("SELECT * FROM contacts WHERE first_name LIKE ? OR last_name LIKE ? OR phone_number LIKE ?",
              ('%'+query+'%', '%'+query+'%', '%'+query+'%'))
    rows = c.fetchall()
    if rows:
        print('Результаты поиска:')
        for row in rows:
            print(row)
    else:
        print('Контакты не найдены.')

# функция для удаления контакта
def delete_contact(query):
    c.execute("DELETE FROM contacts WHERE id=? OR first_name LIKE ? OR last_name LIKE ? OR phone_number LIKE ?",
              ('%'+query+'%', '%'+query+'%', '%'+query+'%', '%'+query+'%'))
    conn.commit()
    print('Контакт успешно удален!')

# функция просмотра всех контактов
def show_data():
    # c.execute("SELECT * FROM contacts ORDER BY first_name")
    # for row in c.fetchall():
    #     print(row)
    tel = pd.read_sql("SELECT * FROM contacts ORDER BY first_name")
    return tel

# def save():
#     with open("contacts.json", "w", encoding="utf-8") as fh:
#         fh.write(json.dumps(contact, ensure_ascii=False))
#     print("Контакты успешно сохранены в файле contacts.json")


# add_contact('Иван', 'Васин', '1277567  25578090', 'ivaov@mail.com', 'Друзья')
# add_contact('Петр', 'Жиглов', '2345645', 'jiglov@mail.com', 'Коллеги')
# add_contact("Алексей","Сидоров","875645 976456","alek@mail.com","Семья")






# command = input("Введите команду: ")
# if command ==  "add":
#     name = input("Введите имя нового контакта: ")
#     last_name = input("Введите фамилию: ")
#     number0 = input("Введите 1й номер: ")
#     number1 = input("Введите 2й номер: ")
#     mail = input("Введите email: ")
#     category = input("Введите категорию: ")
#     telephon = number0 +" "+number1
#
#     add_contact(name,last_name,telephon,mail,category)
# elif command == "all":
#     print("Список контактов")
#     show_data()
#
# elif command == "find":
#     query = input("Введите данные контакта  для поиска: ")
#     search_contacts(query.title())
#     # elif command == "save":
#     #     print("запись контактов в JSON")
#     #     save()
# elif command == "del":
#     query = input("Введите данные контакта для удаления: ")
#     delete_contact(query)
# elif command == "help":
#     for h in help_:
#         print(h)
# elif command == "stop":
#         # закрытие соединения с базой данных
#     conn.close()
#     print("пока")

# закрытие соединения с базой данных
conn.close()