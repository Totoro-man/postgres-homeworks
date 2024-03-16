import json

import psycopg2

from config import config

from utils.utils import *


def main():
    script_file = 'fill_db.sql'
    json_file = 'suppliers.json'
    db_name = 'hw5'

    params = config()
    conn = None

    create_database(params, db_name)
    print(f"БД {db_name} успешно создана")

    params.update({'dbname': db_name})
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                execute_sql_script(cur, script_file)
                print(f"БД {db_name} успешно заполнена")

                create_suppliers_table(cur)
                print("Таблица suppliers успешно создана")

                suppliers = get_suppliers_data(json_file)
                insert_suppliers_data(cur, suppliers)
                print("Данные в suppliers успешно добавлены")

                add_foreign_keys(cur, json_file)
                print(f"FOREIGN KEY успешно добавлены")

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def create_database(params, db_name) -> None:
    """Создает новую базу данных."""
    bu = BaseUtils('admin', db_name)
    bu.init_base()
    del bu


def execute_sql_script(cur, script_file) -> None:
    """Выполняет скрипт из файла для заполнения БД данными."""
    f = open(script_file, 'r', encoding='utf-8')
    queries = f.read()
    cur.execute(queries)


def create_suppliers_table(cur) -> None:
    """Создает таблицу suppliers."""
    query = '''CREATE TABLE suppliers (
                supplier_id serial PRIMARY KEY,
                company_name varchar,
                contact varchar,
                address varchar,
                phone varchar,
                fax varchar,
                homepage varchar,
                products varchar );'''
    cur.execute(query)


def get_suppliers_data(json_file: str) -> list[dict]:
    """Извлекает данные о поставщиках из JSON-файла и возвращает список словарей с соответствующей информацией."""
    with open(json_file, 'r', encoding='utf-8') as json_data:
        data = json.load(json_data)
        for i in data:
            print(i)
    return data


def insert_suppliers_data(cur, suppliers: list[dict]) -> None:
    """Добавляет данные из suppliers в таблицу suppliers."""
    for i in suppliers:
        values_data = ""
        for j in list(i.values())[:-1]:
            values_data = values_data + f"'{str(j).replace("'", "''")}',"
        for j in i.get('products'):
            query = (f"INSERT INTO suppliers ({','.join(list(i.keys()))})"
                     f"VALUES ({values_data}'{j.replace("'", "''")}')")
            cur.execute(query)


def add_foreign_keys(cur, json_file) -> None:
    """Добавляет foreign key со ссылкой на supplier_id в таблицу products."""
    pass


if __name__ == '__main__':
    main()
