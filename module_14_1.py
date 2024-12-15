"""
coding: utf-8
Дегтярев Виталий (группа 22/08)
Домашнее задание №14.1
Домашнее задание по теме "Создание БД, добавление, выбор и удаление элементов."
"""

import sqlite3

# Подключение к БД и создание курсора
connection = sqlite3.connect("not_telegram.db")
cur = connection.cursor()

# Создание таблицы
cur.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

# Заполнение таблицы 10 записями:
for i in range(1, 11):
    cur.execute(" INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)", (f"User{i}",
                        f"example{i}@gmail.com", f"{i*10}", "1000"))

# Обновление balance у каждой 2ой записи начиная с 1ой на 500:
cur.execute("UPDATE Users SET balance = ? WHERE id % 2 != 0", (500,))

# Удаление каждой 3-й записи в таблице начиная с 1ой (придумал только перечислением Id строк):
cur.execute("DELETE FROM Users WHERE id IN (1, 4, 7, 10)") # Не получилось кортеж в параметры занести

# Вывод записей в консоль кроме пользователя у которого возраст = 60
cur.execute("SELECT * FROM Users WHERE Age != ?", (60,))
users = cur.fetchall()
for user in users:
    print(f'Имя:{user[1]} | Почта:{user[2]} | Возраст:{user[3]} | Баланс:{user[4]}')

connection.commit()
connection.close()