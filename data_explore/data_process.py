# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 21:05:47 2024

@author: adamw
"""
import sys
sys.path.append('../')
import pandas as pd
from utils.config_handler import ConfigHandler
from utils.database_handler import DatabaseHandler

class DataManager:
    # Handles data processing for the database.
    def __init__(self, database_name, config_name):
        # Initialise config and database.
        config_handler = ConfigHandler("config")
        self.config = config_handler.read_config(config_name)
        self.database = DatabaseHandler(database_name)
        
    def load_csv(self, file_path):
        # Load main csv.
        df = pd.read_csv(file_path)
        # A sample can be used to speed up the process for testing or demonst.
        df = df.sample(frac=self.config.get("SAMPLE_FRAC"), random_state=1)
        return df
        
    def split_column(self, df, column_name, delimiter=','):
        # Split the given data by commas.
        locations_split = df[column_name].str.split(delimiter, expand=True)
        locations_split.columns = [f"{column_name}_{i+1}" for i in range(locations_split.shape[1])]
        expanded_df = pd.concat([df, locations_split], axis=1)  
        return expanded_df
        
    def format_datetime(self, table):
        # Format the column as a set date time.
        query = self.config.get("DATE_PROCESSING")
        df = self.database.query_database(query)
        self.database.create_database_table(df, table)
        return df
    
    def format_stations(self, table):
        # Format the stations to split the columns by commas to get the station area.
        query = self.config.get("STATION_PROCESSING")
        df = self.database.query_database(query)
        df = self.split_column(df, "Station_Name")
        self.database.create_database_table(df, table)
    
    def organise_data(self, df):
        # Initial Processing of dataframe.
        df_trip = df[["Rental_ID","Bike_ID","Start_Station_ID", "End_Station_ID", "Start_Date", "End_Date", "Duration_ms"]]
        df_bike = df[["Bike_ID","Bike_Model"]].drop_duplicates()
        start_station_df = df[['Start_Station_ID', 'Start_Station_Name']].drop_duplicates()
        start_station_df.columns = ['Station_ID', 'Station_Name']
        end_station_df = df[['End_Station_ID', 'End_Station_Name']].drop_duplicates()
        end_station_df.columns = ['Station_ID', 'Station_Name']
        df_station = pd.concat([start_station_df, end_station_df]).drop_duplicates().reset_index(drop=True)
        # Uploading dataframes as tables.
        # trips table has primary key of Rental_ID and secondary keys of Bike_ID, Start_StationID and End_Station_ID.
        self.database.create_database_table(df_trip, "trips")
        # bikes table has primary key of Bike_ID and can join to trips table.
        self.database.create_database_table(df_bike, "bikes")
        # stations has primary key of station_ID and can join tbl trips table.
        self.database.create_database_table(df_station, "stations")
        # Final Processing of tables.
        self.format_datetime("trips")
        self.format_stations("stations")
        
def main():
    data_manager = DataManager("cycle", "data_process")
    df = data_manager.load_csv("../final_data/cycledata_combined.csv")
    data_manager.organise_data(df)

if __name__ == "__main__":
    main()