"""
coding: utf-8
Дегтярев Виталий (группа 22/08)
Домашнее задание №14.5
Домашнее задание по теме "Написание примитивной ORM"

МОДУЛЬ CRUD-ФУНКЦИЙ
"""


import sqlite3


# Функция создает таблицы Users, Products - если они еще не созданы
def initiate_db():
    connection = sqlite3.connect("files/database.db")
    cur = connection.cursor()

    # Создание таблицы Users
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL
    )
    ''')

    # Создание таблицы Products
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    ''')

    connection.commit()
    connection.close()


# Функция возвращает все записи из таблицы Products
def get_all_products():
    connection = sqlite3.connect("files/database.db")
    cur = connection.cursor()
    cur.execute("SELECT * FROM Products")
    products = cur.fetchall()
    connection.close()
    return products


# Функция добавления в таблицу Users нового пользователя
def add_user(username, email, age):
    connection = sqlite3.connect("files/database.db")
    cur = connection.cursor()

    cur.execute(f'''
    INSERT INTO Users (username, email, age, balance) VALUES ('{username}', '{email}', '{age}', '1000')
    ''')

    connection.commit()
    connection.close()


# Функция проверки наличия пользователя в таблице Users
def is_included(username):
    connection = sqlite3.connect("files/database.db")
    cur = connection.cursor()

    check_user = cur.execute("SELECT * FROM Users WHERE username = ?", (username,)).fetchone()
    connection.close()
    if check_user is None:
        return False
    else:
        return True


# initiate_db()