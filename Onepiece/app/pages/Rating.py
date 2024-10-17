# importing os ans sys modules
import os

# MySQL connector
import mysql.connector

# Pandas
import pandas as pd

# importing os module for environment variables
import os

# importing necessary functions from dotenv library
from dotenv import load_dotenv

# loading variables from .env file
load_dotenv() 

import dash
from dash import html, dcc, callback, Input, Output
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

# Create dataframe of One Piece data 
query = f"Select * from {table_name}"
onepiece_data = db_query(db_config,query)

dash.register_page(__name__)

# Build dash app layout
layout = html.Div(children=[ html.H1('One piece Rating', 
                                style={'textAlign': 'center', 'color': 'blue',
                                'font-size': 30}),

                                # Input
                                html.Div(["Input Year: ", dcc.Input(id='input-year', value='1999', min='1999',max = '2024', 
                                type='number', style={'height':'40px', 'font-size': 20}),], 
                                style={'font-size': 20}),
                                html.Br(),

                                # Segment
                                html.Div([
                                        html.Div(dcc.Graph(id='yearly-rate-bar-plot')),
                                        html.Div(dcc.Graph(id='yearly-rate-line-plot'))
                                ], style={'display': 'flex'}),

                                # Slider
                                        html.Label('Season'),
                                        dcc.Slider(
                                            id = 'slider-season',
                                            min=1,
                                            max=21,
                                            step=None,
                                            marks={i: str(i) for i in range(1, 22)},
                                            value=1,
                                        ),
                                html.Br(),

                                # Segment
                                html.Div([
                                        html.Div(dcc.Graph(id='season-rate-bar-plot',style={'color':'red'})),
                                        html.Div(dcc.Graph(id='season-rate-line-plot'))
                                ], style={'display': 'flex'}),
                                ])


def compute_year_info(onepiece_data, entered_year):
    """ Compute_info function description

    This function takes in One piece data and selected year as an input and performs computation for creating charts and plots.

    Arguments:
        onepiece_data: Input One piece data.
        entered_year: Input year for which computation needs to be performed.

    Returns:
        Computed average dataframes for rate.

    """
    # Select data
    df =  onepiece_data[onepiece_data['Year']==int(entered_year)]
    # Compute average rate
    avg_rate = df.groupby(['Month'])['Rate'].mean().reset_index()
    return avg_rate


def compute_season_info(onepiece_data, entered_season):
    """ Compute_info function description

    This function takes in One piece data and selected year as an input and performs computation for creating charts and plots.

    Arguments:
        onepiece_data: Input One piece data.
        entered_season: Input season for which computation needs to be performed.

    Returns:
        Computed average dataframes for rate.

    """
    # Select data
    df =  onepiece_data[onepiece_data['Season']==int(entered_season)]
    # Compute average rate
    rate = df[["Episod_season","Rate"]].reset_index()
    return rate


"""Callback Function

Function that returns fugures using the provided input year.

Arguments:

    entered_year: Input year provided by the user.

Returns:

    List of figures computed using the provided helper function `compute_info`.
"""
# Callback decorator for yearly rate
@callback( [
               Output(component_id='yearly-rate-bar-plot', component_property='figure'),
               Output(component_id='yearly-rate-line-plot', component_property='figure'),
               ],
               Input(component_id='input-year', component_property='value'))

def get_yealy_graph(entered_year):

    # Compute required information for creating graph from the data
    avg_rate = compute_year_info(onepiece_data, entered_year)

    # Bar plot for carrier delay
    bar_fig = px.bar(avg_rate, x='Month', y='Rate', title='Average rating by month')
    # Line plot for carrier delay
    line_fig = px.line(avg_rate, x='Month', y='Rate', title='Average rating by month')

    return[bar_fig, line_fig]

# Callback decorator for season rate
@callback( [
               Output(component_id='season-rate-bar-plot', component_property='figure'),
               Output(component_id='season-rate-line-plot', component_property='figure'),
               ],
               Input(component_id='slider-season', component_property='value'))

def get_season_graph(entered_season):

    # Compute required information for creating graph from the data
    rate = compute_season_info(onepiece_data, entered_season)

    # Bar plot for carrier delay
    bar_fig = px.bar(rate, x='Episod_season', y='Rate', title='Rating by episod')
    # Line plot for carrier delay
    line_fig = px.line(rate, x='Episod_season', y='Rate', title='Rating by episod')

    return[bar_fig, line_fig]


