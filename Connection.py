import pymysql
import psycopg2
import pyodbc


class Connection(object):
    def __init__(self, host, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db


    def connect_mysql(self):
        conn = pymysql.connect(
            host = self.host,
            port = 3306,
            user = self.user,
            passwd = self.password,
            db = self.db
        )
        return conn


    def connect_postgres(self):
        conn = psycopg2.connect(
            host = self.host,
            database = self.db,
            user = self.user,
            password = self.password
        )
        return conn


    def connect_sql_server(self):
        conn = pyodbc.connect(r'DRIVER={SQL Server};'r'SERVER=' + self.host + ';'r'DATABASE=' + self.db + ';'r'UID=' + self.user + ';'r'PWD=' + self.password + '')
        return conn