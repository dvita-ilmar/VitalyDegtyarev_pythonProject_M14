"""
coding: utf-8
Дегтярев Виталий (группа 22/08)
Домашнее задание №14.4
Домашнее задание по теме "План написания админ панели"

МОДУЛЬ CRUD-ФУНКЦИЙ
"""


import sqlite3


# Функция создает таблицу Products
def initiate_db():
    connection = sqlite3.connect("files/database.db")
    cur = connection.cursor()
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