import dash
from dash import Dash, html, dcc

image_path = 'assets/One-piece-Top2.jpg'

app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    html.Div([html.Img(src = image_path,
            style={
            'height': '40%',
            'width': '40%'
            })], style={'textAlign': 'center'}),
    html.Div([
            dcc.Link(f"{page['name']}" + " | " , href=page["relative_path"])
            for page in dash.page_registry.values()
    ], style={'textAlign': 'center'}),
        html.Hr(),

    # Content of each page
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)