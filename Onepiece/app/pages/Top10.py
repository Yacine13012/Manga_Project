# MySQL connector
import mysql.connector

# Pandas
import pandas as pd

# Numpy
import numpy as np

# importing os module for environment variables
import os

# importing necessary functions from dotenv library
from dotenv import load_dotenv

# loading variables from .env file
load_dotenv() 

import dash
from dash import html, dcc, callback, dash_table, Input, Output
import plotly.express as px

# Initialize variables
host = os.getenv("MYSQL_HOSTNAME")
user = os.getenv("MYSQL_USERNAME")
password = os.getenv("MYSQL_PASSWORD")
database = "manga"
table_name = "Onepiece"
manga_name = "One piece"

# MySQL database connection details
db_config = {
    'host': host,
    'user': user,
    'password': password,
    'database': database
}

def db_query(config,query):

# Function to connect into the database,send a query and save the result to a Dataframe

    # Establish a connection to the MySQL database
    conn = mysql.connector.connect(**config)

        # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

        # Execute the query and fetch the results
    cursor.execute(query)
    results = cursor.fetchall()

        # Create a Pandas DataFrame from the extracted data
    columns = [column[0] for column in cursor.description]
    df = pd.DataFrame(results, columns=columns)

        # Close the database connection
    cursor.close()
    conn.close()

    return(df)


# Create dataframe of Top10 One Piece episods
query = f"Select * from {table_name} "
onepiece_data = db_query(db_config,query)

default_options = [
    {"label": "All", "value": 0},
    {"label": "Season 1", "value": 1},
    {"label": "Season 2", "value": 2},
    {"label": "Season 3", "value": 3},
    {"label": "Season 4", "value": 4},
    {"label": "Season 5", "value": 5},
    {"label": "Season 6", "value": 6},
    {"label": "Season 7", "value": 7},
    {"label": "Season 8", "value": 8},
    {"label": "Season 9", "value": 9},
    {"label": "Season 10", "value": 10},
    {"label": "Season 11", "value": 11},
    {"label": "Season 12", "value": 12},
    {"label": "Season 13", "value": 13},
    {"label": "Season 14", "value": 14},
    {"label": "Season 15", "value": 15},
    {"label": "Season 16", "value": 16},
    {"label": "Season 17", "value": 17},
    {"label": "Season 18", "value": 18},
    {"label": "Season 19", "value": 19},
    {"label": "Season 20", "value": 20},
    {"label": "Season 21", "value": 21},

]


dash.register_page(__name__)

# Build dash app layout
layout = html.Div([
    html.H1(children='One piece top 10',
            style={'textAlign': 'center', 'color': '#503D36',
                    'font-size': 30}          
            ),

    # Dropdown
    dcc.Dropdown(
        options = default_options,
        value = 0,id="dropdown"
        ),
    html.Br(),
    html.Br(), 

    # Table
    dash_table.DataTable(
        id='table',
        columns=[{'name': i, 'id': i} for i in ["Rank","Season","Episod_season","Title","Rate"]],
        data=onepiece_data.to_dict('records'),
        style_table={'overflowX': 'auto'}
    )
])

@callback(
    Output('table', 'data'),
    Input('dropdown', 'value')
)
def update_table(season):
    if season ==0:
        filtered_df = onepiece_data.sort_values("Rate",ascending = False).head(10)
    else:    
        filtered_df = onepiece_data[onepiece_data['Season'] == season].sort_values("Rate",ascending = False).head(10)
    filtered_df = filtered_df[["Season","Episod_season","Title","Rate"]]
    filtered_df["Rank"] = np.arange(1, len(filtered_df) + 1)
    return filtered_df.to_dict('records')



