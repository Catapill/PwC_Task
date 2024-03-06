# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 21:05:47 2024

@author: adamw
"""
import sys
sys.path.append('../')
from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
from utils.config_handler import ConfigHandler

class DataGather:
    # Handles extracting data from website.
    def __init__(self, config):
        # Initialise config and other class parameters.
        self.config = config
        self.source = self.config.get("SOURCE")
        self.save_path = self.config.get("SAVE_PATH")
        
    def extract_links_from_webpage(self):
        # Extracts all links from the website based on requirements defined in config.
        links = []
        webpage = self.config.get("SOURCE")
        with open(f"../{webpage}", 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            for link in soup.find_all('a'):
                link_text = link.text
                if "JourneyDataExtract" in link_text and any(x in link_text for x in self.config.get("REQUIREMENTS_ANY")):
                    links.append(link.get('href'))
        return links
    
    def download_link(self, links):
        # Downloads csv files from list of links.
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        for i, link in enumerate(links):
            response = requests.get(link)
            with open(f"{self.save_path}/cycledata_{i}.csv", 'wb') as f:
                f.write(response.content)
        
    def combine_data(self):
        # Combines the data into one csv file.
        rename_dict = {
            "Rental Id":"Rental_ID",
            "Number":"Rental_ID",
            "Start Date":"Start_Date",
            "Start date":"Start_Date",
            "Bike Id":"Bike_ID",
            "Bike number":"Bike_ID",
            "Bike model":"Bike_Model",
            "End Date":"End_Date",
            "End date":"End_Date",
            "StartStation Id":"Start_Station_ID",
            "End station number":"End_Station_ID",
            "Start station number":"Start_Station_ID",
            "EndStation Id":"End_Station_ID",
            "StartStation Name":"Start_Station_Name",
            "Start station":"Start_Station_Name",
            "EndStation Name":"End_Station_Name",
            "End station":"End_Station_Name",
            "Total duration":"Duration",
            "Total duration (ms)":"Duration_ms",
        }
        all_data = pd.DataFrame()
        df_list = []
        # Iterate through each file in the folder
        for file_name in os.listdir(self.save_path):
            if file_name.endswith('.csv'):
                
                file_path = os.path.join(self.save_path, file_name)
                df = pd.read_csv(file_path)
                # Converts Duration to match Duration_ms column. and different links have different formats.
                try:
                    df["Duration_ms"] = df["Duration"]*1000
                except Exception:
                    pass
                df = df.rename(columns=rename_dict)
                # Drops Duration column as this format is awkward for data analysis
                df.drop(columns="Duration", inplace=True)
                df_list.append(df)
        # Concatenate the DataFrame into one.
        all_data = pd.concat(df_list, ignore_index=True)
        if not os.path.exists("../final_data"):
            os.makedirs("../final_data")
        all_data.to_csv("../final_data/cycledata_combined.csv", index=False)  
    
def main():
    config_handler = ConfigHandler("config")
    config = config_handler.read_config("data_gather")
    data_gather = DataGather(config)
    links = data_gather.extract_links_from_webpage()
    data_gather.download_link(links)
    data_gather.combine_data()

if __name__ == "__main__":
    main()