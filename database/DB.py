from configparser import ConfigParser
import sqlite3


def prepare_update_array_from(data_array):
    data_string = ""
    for data_key in data_array:
        new_data_string = data_key + " = " + "'" + data_array[data_key] + "'"
        if data_string:
            data_string = ", ".join([data_string, new_data_string])
        else:
            data_string = new_data_string
    return data_string


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

    def db_where(self, column, value):
        query = "SELECT * FROM %s WHERE %s = '%s'"
        query = query % (self.db_table, column, value)
        self.cursor = self.execute(query)
        return self

    def fetch_all(self):
        query = '''SELECT * FROM %s'''
        query = query % self.db_table
        cursor = self.execute(query)
        return cursor.fetchall()

    def db_get(self):
        return self.cursor.fetchall()

    def fetch_one(self):
        return self.cursor.fetchone()

    def create(self, data_array):
        query = "INSERT INTO %s (%s) VALUES ('%s')"
        columns = ', '.join(data_array.keys())
        values = "', '".join(data_array.values())
        query = query % (self.db_table, columns, values)
        self.execute(query)
        self.connection.commit()
        return

    def update(self, reference_column, reference_value, data_array):
        update_array = prepare_update_array_from(data_array)
        print(update_array)
        query = '''
        UPDATE %s
        SET %s 
        WHERE %s = '%s' 
        '''
        query = query % (self.db_table, update_array, reference_column, reference_value)
        print(query)
        self.execute(query)
        self.connection.commit()
        return


