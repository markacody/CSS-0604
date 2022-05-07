from dash import html
from components.navbar import create_navbar

nav = create_navbar()

header = html.H2('Learning Analytics Home')

def display_home():
    layout = html.Div([
        nav,
        header,
    ])
    return layout