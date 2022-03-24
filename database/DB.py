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

