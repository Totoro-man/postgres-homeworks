"""Скрипт для заполнения данными таблиц в БД Postgres."""
import psycopg2
from psycopg2 import sql
import csv

PASSWORD = "admin"
DATABASE_NAME = "north_data"


def check_database_exist():
    with check.cursor() as cur:
        query = f"SELECT datname FROM pg_catalog.pg_database WHERE datname = '{DATABASE_NAME}'"
        cur.execute(query)
        result = bool(cur.rowcount)
    return result


def create_database():
    with check.cursor() as cur:
        cur.execute(sql.SQL('CREATE DATABASE {};').format(sql.Identifier(DATABASE_NAME)))


def create_tables():
    f = open('create_tables.sql', 'r')
    queries = f.read().split(';')
    with conn.cursor() as cur:
        for i in queries:
            cur.execute(i)


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


def fill_table_customers():
    data = []
    with open('north_data/customers_data.csv', 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if not line_count == 0:
                data.append(row)
            line_count += 1
    query = f'INSERT INTO customers VALUES (%s, %s, %s)'
    with conn.cursor() as cur:
        cur.executemany(query, data)


def fill_table_employees():
    data = []
    with open('north_data/employees_data.csv', 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if not line_count == 0:
                data.append(row)
            line_count += 1
    query = f'INSERT INTO employees VALUES (%s, %s, %s, %s, %s, %s)'
    with conn.cursor() as cur:
        cur.executemany(query, data)


def fill_table_orders():
    data = []
    with open('north_data/orders_data.csv', 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if not line_count == 0:
                data.append(row)
            line_count += 1
    query = f'INSERT INTO orders VALUES (%s, %s, %s, %s, %s)'
    with conn.cursor() as cur:
        cur.executemany(query, data)


check = psycopg2.connect(
    database="postgres",
    user='postgres',
    password=PASSWORD,
    host='localhost',
    port='5432'
)
check.autocommit = True

if not check_database_exist():
    create_database()
check.close()

conn = psycopg2.connect(
    database="north_data",
    user='postgres',
    password=PASSWORD,
    host='localhost',
    port='5432'
)

create_tables()
# conn.commit()
# conn.close()

fill_table_customers()
fill_table_employees()
fill_table_orders()

conn.commit()
conn.close()
