from dash import html
from components.navbar import create_navbar

nav = create_navbar()

header = html.H2('Course Analytics')

def display_course():
    layout = html.Div([
        nav,
        header,
    ])
    return layout