import dash
from dash import html, dcc, callback, Input, Output

image_path = 'assets/one-piece-4k.jpeg'

dash.register_page(__name__,path= "/") # '/' is the main page

# Build dash app layout
layout = html.Div([html.Img(src=image_path)])


