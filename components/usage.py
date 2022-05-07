from dash import html
from components.navbar import create_navbar

nav = create_navbar()

header = html.H2('Usage Analytics')

def display_usage():
    layout = html.Div([
        nav,
        header,
    ])
    return layout