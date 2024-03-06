# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 14:39:32 2024

@author: adamw
"""
import sys
sys.path.append('../')
import sqlite3
from pandas import read_sql

class DatabaseHandler:
    def __init__(self, database_name):
        # Initialise database name.
        self.database_name = database_name
        
    def create_database_table(self, data, table_name):
        # Create a table in the db.
        with sqlite3.connect(f"../{self.database_name}.db") as conn:
            
            data.to_sql(table_name, conn, index=False, if_exists='replace')
            conn.commit()
    
    def query_database(self, query):
        # Query the database.
        with sqlite3.connect(f"../{self.database_name}.db") as conn:
            df = read_sql(query, conn)
        return df