"""
Created on Tue May 18 10:14:57 2021

@author: massimo
"""
from . import config, mysql


class MySQLConnector:
    """Connects to the underlying MySQL database"""

    def __init__(self):
        self.connection = None
        self.cursor = None

        pw = config('mysql_root_pw')

        self.connect_to_mysql_instance(passwd=pw)

    def connect_to_mysql_instance(self, host='localhost',
                                  user='root', passwd=''):
        try:
            self.connection = mysql.connector.connect(host=host, user=user,
                                                      passwd=passwd)
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as e:
            print('Error %s occurred while connecting.' % e)

    def connect_to_db(self, db_name):
        self.connection.database = db_name

    @staticmethod
    def get_db_list():
        db_list = config('DB_LIST').replace("\"", "")
        db_list = db_list[1:-1].split(",")
        return db_list

    def get_table_list(self):
        self.cursor.execute('show tables')
        tables = []
        for t in self.cursor.fetchall():
            tables.append(*t)
        return tables

    def get_table_description(self, table_name):
        self.cursor.execute(f'describe {table_name}')
        fields = [('Field', 'Type', 'Null', 'Key', 'Default', 'Extra')]
        for e in self.cursor.fetchall():
            fields.append(e)
        return fields

    def get_fields(self, table):
        self.cursor.execute(f'describe {table}')
        fields = []
        for row in self.cursor.fetchall():
            fields.append(row[0])
        return fields

    def execute_read_query(self, query):
        """
        query = select, from_, where, operator, condition
        """

        select = ', '.join(query[0]) or '*'
        from_ = query[1]
        where = query[2]
        if not where:
            string = f"""SELECT {select}
                          FROM {from_};"""
        else:
            operator = query[3] or 'regexp'
            condition = query[4] if operator != 'regexp' else '\'.*' + query[4] + '.*\''
            string = f"""SELECT {select}
                         FROM {from_}
                         WHERE {where} {operator} {condition};"""
        rows = []
        self.cursor.execute(string)
        rows.append(self.cursor.fetchall())
        return rows

    def close_connection(self):
        self.cursor.close()
        self.connection.close()
