"""Скрипт для заполнения данными таблиц в БД Postgres."""
from utils.utils import *
import csv

PASSWORD = "admin"
DATABASE_NAME = "north"


def read_data_file(file_name: str):
    data = []
    with open(file_name, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if not line_count == 0:
                data.append(row)
            line_count += 1
    return data


def fill_table(file_name: str, table_name: str, fields_amount: int):
    data = read_data_file(file_name)
    placeholder = ', '.join(['%s' for i in range(fields_amount)])
    query = f'INSERT INTO {table_name} VALUES ({placeholder})'
    with conn.cursor() as cur:
        cur.executemany(query, data)


"""
    В этом блоке:
    Проверяем существование базы DATABASE_NAME
    Создаем ее если нет
"""
b_utils = BaseUtils(PASSWORD, DATABASE_NAME)
b_utils.init_base()

"""
    В этом блоке:
    Создаем таблицы скриптами из файла create_tables.sql
    Заполняем созданные таблицы
"""
conn = psycopg2.connect(
    database=DATABASE_NAME,
    user='postgres',
    password=PASSWORD,
    host='localhost',
    port='5432'
)

o_util = OtherUtils(conn)
o_util.execute_sql_from_file('create_tables.sql',True)

fill_table('north_data/customers_data.csv', 'customers', 3)
fill_table('north_data/employees_data.csv', 'employees', 6)
fill_table('north_data/orders_data.csv', 'orders', 5)

conn.commit()
conn.close()
