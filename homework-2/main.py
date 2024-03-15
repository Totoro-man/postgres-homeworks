from utils.utils import *
import csv

PASSWORD = "admin"
DATABASE_NAME = "northwind"

"""
    В этом блоке:
    Проверяем существование базы DATABASE_NAME
    Создаем ее если нет
"""
b_utils = BaseUtils(PASSWORD, DATABASE_NAME)
b_utils.init_base()

"""
    В этом блоке:
    Выполняем скрипты из файла northwind_script.sql
"""
conn = psycopg2.connect(
    database=DATABASE_NAME,
    user='postgres',
    password=PASSWORD,
    host='localhost',
    port='5432'
)

o_util = OtherUtils(conn)
o_util.execute_sql_from_file('northwind_script.sql')

conn.commit()
conn.close()
