import sqlite3

# connection = ''
# cursor = ''

# try:
#     connection = sqlite3.connect('example.db')
#     cursor = connection.cursor()
#     print('Successful connection...')
# except Exception as e:
#     print('Error: ', e)


try:
    # Используем контекстный менеджер для соединения с базой данных
    with sqlite3.connect('example.db') as connection:
        print('Successful connection...')
        # Создаем курсор внутри контекстного менеджера
        cursor = connection.cursor()
        # Пример запроса
        cursor.execute("SELECT sqlite_version();")
        version = cursor.fetchone()
        print('SQLite version:', version[0])
except Exception as e:
    print('Error: ', e)

############################################

# Создать таблицу если не существует

############################################


# try:
#     cursor.execute('''
#                 CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 name TEXT NOT NULL,
#                 age INTEGER NOT NULL)
#                 ''')
#     print('The table was crearted')
#     connection.commit()
# except Exception as e:
#     print(e)


############################################

# Добавить данные в таблицу

############################################


# try:
#     cursor.execute('''
#         INSERT INTO users (name,age) VALUES
#                    ('Alice',25),
#                    ('Bob',30)
#     ''')
#     print("The data has been appdated")
#     connection.commit()
# except Exception as e:
#     print(e)


############################################

# Прочитать данные

############################################

# cursor.execute('SELECT * FROM users')
# rows = cursor.fetchall()

# print("Data int the table:")
# for row in rows:
#     print(row)


############################################

# Обновление данных

############################################

# cursor.execute('''
# UPDATE users SET age = 26 WHERE name = 'Alice'
# ''')

# print("Data was apdated")
# connection.commit()

############################################

# Удаляем данные

############################################

# cursor.execute('''
# DELETE FROM users WHERE name = 'Bob'
# ''')

# print("Data was deleted.")
# connection.commit()

############################################

# Закрыть соеденинение

############################################

# connection.close()
# print("Соединение с базой данных закрыто.")
