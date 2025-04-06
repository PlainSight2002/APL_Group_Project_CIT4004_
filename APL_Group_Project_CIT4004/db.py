'''
Authors
Sassania Hibbert 1901201
Darrell King 1803342
Shavar Mclean 1903893
Mark Vernon 1908916
Jelani Jackson 1901811
'''

# Connects to a SQL database using pyodbc
import sys

import pyodbc
import json


class DB:

    @staticmethod
    def create_server_connection():

        with open('dbconfig.json', 'r') as fh:
            config = json.load(fh)

        connection_string = f"DRIVER={config['DRIVER']};SERVER={config['SERVER']};DATABASE={config['DATABASE']};UID={config['USERNAME']};PWD={config['PASSWORD']}"

        connection = None
        try:
            connection = pyodbc.connect(connection_string)
            print("MySQL Database connection successful")
        except pyodbc.Error as err:
            print("Connection failed")
        return connection

    @staticmethod
    def execute_query(query):

        try:
            conn = DB.create_server_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            conn.close()
            return True

        except Exception as e:
            return False

    @staticmethod
    def execute_query_params(query, params):

        try:
            conn = DB.create_server_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            conn.close()
            return True

        except BaseException as e:
            # Get current system exception
            ex_type, ex_value, ex_traceback = sys.exc_info()
            print(f"ERROR: {ex_value}")
            return False
