from configparser import ConfigParser
import sqlite3


class DB:

    connection = None
    db_table = None
    cursor = None

    def __init__(self):
        self.config_file = 'config.ini'
        self.config = ConfigParser()
        self.config.read(self.config_file)
        self.database_name = self.config.get('database', 'database_name')
        self.connect()

    def connect(self):
        self.connection = sqlite3.connect(self.database_name)
        self.cursor = self.connection.cursor()
        return self.connection

    def execute(self, query, params = None):
        self.cursor.execute(query)
        return self.cursor

    def table(self, table):
        self.db_table = table
        return self

    def where(self, column, value):
        query = "SELECT * FROM %s WHERE %s = '%s'"
        query = query % (self.db_table, column, value)
        print(query)
        self.cursor = self.execute(query)
        return self

    def all(self):
        query = '''SELECT * FROM %s'''
        query = query % self.db_table
        cursor = self.execute(query)
        return cursor.fetchall()

    def get(self):
        return self.cursor.fetchall()

    def first(self):
        return self.cursor.fetchone()

    def create(self, data_array):
        query = "INSERT INTO %s (%s) VALUES ('%s')"
        columns = ', '.join(data_array.keys())
        values = "', '".join(data_array.values())
        query = query % (self.db_table, columns, values)
        print(query)
        self.execute(query)
        self.connection.commit()
        return

    def update(self, reference_column, reference_value, data_array):
        update_array = self.prepare_update_array_from(data_array)
        query = '''
        UPDATE %s
        SET %s 
        WHERE %s = %s 
        '''
        query = query % (self.db_table, update_array, reference_column, reference_value)

    def prepare_update_array_from(self, data_array):


