from database.db_instance import db_connection
import asyncio
import time


async def some_function():
    async with db_connection:
        users = await db_connection.get_all_users()
        print(users)


async def main():
    x1 = time.time()

    await some_function()

    print(time.time() - x1)


if __name__ == "__main__":
    asyncio.run(main())

#
# import mysql.connector
#
# # Параметры подключения к базе данных
# config = {
#     'user': 'timur',
#     'password': '',
#     'host': '51.250.64.64',
#     'database': ''
# }
#
# # Подключение к базе данных
# try:
#     connection = mysql.connector.connect(**config)
#     print("Успешное подключение к базе данных")
#
#     # Здесь вы можете выполнять операции с базой данных
#
#     # Закрытие соединения
#     connection.close()
#     print("Соединение с базой данных закрыто")
#
# except mysql.connector.Error as error:
#     print("Ошибка при подключении к базе данных: {}".format(error))
