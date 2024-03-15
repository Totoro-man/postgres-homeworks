import psycopg2
import json
from psycopg2 import sql


class BaseUtils:

    def __init__(self, password: str, database_name: str):
        self.conn = psycopg2.connect(
                    database="postgres",
                    user='postgres',
                    password=password,
                    host='localhost',
                    port='5432')
        self.conn.autocommit = True
        self.database_name = database_name
        self.inifile = IniFile()

    def check_database_exist(self):
        if self.inifile.check_param(self.database_name):
            return True
        with self.conn.cursor() as cur:
            query = f"SELECT datname FROM pg_catalog.pg_database WHERE datname = '{self.database_name}'"
            cur.execute(query)
            result = bool(cur.rowcount)
        return result

    def create_database(self):
        with self.conn.cursor() as cur:
            cur.execute(sql.SQL('CREATE DATABASE {};').format(sql.Identifier(self.database_name)))
        self.inifile.update_param({self.database_name: True})

    def stop(self):
        self.conn.close()

    def init_base(self):

        if not self.check_database_exist():
            self.create_database()
        self.stop()


class OtherUtils:

    def __init__(self, conn: psycopg2, database_name: str = ''):
        self.conn = conn
        self.database_name = database_name
        self.inifile = IniFile()

    def execute_sql_from_file(self, file_path: str, repeatable: bool = False):
        if self.inifile.check_param(file_path):
            return
        f = open(file_path, 'r', encoding='utf-8')
        queries = f.read()
        with self.conn.cursor() as cur:
            cur.execute(queries)
        if not repeatable:
            self.inifile.update_param({file_path: True})


class IniFile:

    def __init__(self):
        self.inifile = 'utils.ini'
        self.iniconfig = {}

    def load_ini_file(self):
        try:
            json_file = open(self.inifile, 'r', encoding='utf-8')
            self.iniconfig = json.load(json_file)
        except:
            pass

    def save_ini_file(self):
        with open(self.inifile, 'w', encoding='utf-8') as json_file:
            json.dump(self.iniconfig, json_file)

    def update_param(self, new_param: dict):
        self.iniconfig.update(new_param)
        self.save_ini_file()

    def check_param(self, param: str):
        self.load_ini_file()
        if self.iniconfig.get(param):
            return True
        else:
            return False
