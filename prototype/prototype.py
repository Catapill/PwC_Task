# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 17:06:52 2024

@author: adamw
"""
import sys
sys.path.append('../')
from utils.config_handler import ConfigHandler
from utils.database_handler import DatabaseHandler
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
import plotly.express as px
import plotly.io as pio
pio.renderers.default='browser'

class Prototype:
    # A simple prototype
    def __init__(self, config_name, database_name):
        # Initialise config and database.
        config_handler = ConfigHandler("config")
        self.config = config_handler.read_config(config_name)
        self.database = DatabaseHandler(database_name)
        
    def fetch_data(self):
        # Query the database.
        query = self.config.get("DATA_GATHER")
        df = self.database.query_database(query)
        return df
    
    def visualise_predictions(self, data, x, y, c="Prediction"):
        # Visualise predictions as a scatter graph.
        fig = px.scatter(data, x=x, y=y, color=c)
        fig.show()
        
    def build_model(self):
        # Simple model for unsupervised anomaly detection
        print("Fetching Data.")
        df = self.fetch_data()
        print("Processing Data.")
        df = df.set_index("Bike_ID")
        df_original = df.copy()

        scaler = StandardScaler()
        df = scaler.fit_transform(df)

        print("Building Model.")
        dbscan = DBSCAN(eps=self.config.get("EPSILON"), min_samples=self.config.get("SAMPLES"))
        df_original['Prediction_Value'] = dbscan.fit_predict(df)
        df_original['Prediction'] = ["Normal" if x >= 0 else 'Anomaly' for x in df_original['Prediction_Value']]
        
        print("Evaluating Predictions.")
        self.visualise_predictions(df_original, "Total_Trips", "Unusual_Trips")
        self.visualise_predictions(df_original, "Total_Trips", "Unusual_Trip_Ratio")
        self.visualise_predictions(df_original, "Days_Since_First_Trip", "Days_Since_Last_Trip")
        self.visualise_predictions(df_original, "Total_Trips", "Average_Monthly_Trips")
        self.visualise_predictions(df_original, "Total_Trips", "Prediction")
        self.visualise_predictions(df_original, "Days_Since_First_Trip", "Total_Trips")
        self.visualise_predictions(df_original, "Days_Since_Last_Trip", "Total_Trips")
        self.visualise_predictions(df_original, "Days_Since_Last_Trip", "Average_Trip_Duration")
        self.visualise_predictions(df_original, "Average_Trip_Duration", "Recent_Average_Trip_Duration_Change")
        
        anomalies = df_original[df_original['Prediction'] == "Anomaly"]
        normals = df_original.drop(anomalies.index)
        
        print(anomalies.mean(numeric_only=True))
        print(normals.mean(numeric_only=True))
        
def main():
    prototype = Prototype("prototype", "cycle")
    prototype.build_model()

if __name__ == "__main__":
    main()