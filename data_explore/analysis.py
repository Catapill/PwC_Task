# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 18:06:11 2024

@author: adamw
"""
import sys
sys.path.append('../')
from utils.database_handler import DatabaseHandler
from utils.config_handler import ConfigHandler
import plotly.express as px
import plotly.io as pio
pio.renderers.default='browser'

class Analsis:
    # Runs basic analysis on the data.
    def __init__(self, database_name, config_name):
        # Initialise config and database.
        config_handler = ConfigHandler("config")
        self.config = config_handler.read_config(config_name)
        self.database = DatabaseHandler(database_name)
        
    def run_basic_analysis(self):
        # Runs a list of queries to get basic statistics about data.
        query_output_list = []
        queries = self.config.get("BASIC_QUERIES")
        for query in queries:
            query_df = self.database.query_database(query)
            result = {query_df.columns[0]: query_df.iloc[0, 0]}
            query_output_list.append(result)
        print(query_output_list)
        return query_output_list
    
    def run_graphic_analysis(self):
        # Runs a list of queries to generate graph for data.
        queries = self.config.get("GRAPHIC_QUERIES")
        for query in queries:
            query_df = self.database.query_database(query)
            print(query_df, "\n")
            self.render_graph(query_df, query_df.columns[0], query_df.columns[1], graph_type="line")
    
    def render_graph(self, data, x, y, graph_type="bar"):
        # Renders a graph.
        if graph_type == "bar":
            fig = px.bar(data, x=x, y=y)
        elif graph_type == "line":
            fig = px.line(data, x=x, y=y)
        elif graph_type == "scatter":
            fig = px.scatter(data, x=x, y=y)
        fig.show()
    
def main():
    analyst = Analsis("cycle", "analysis")
    analyst.run_basic_analysis()
    analyst.run_graphic_analysis()

if __name__ == "__main__":
    main()