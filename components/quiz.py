from dash import html
from components.navbar import create_navbar

nav = create_navbar()

header = html.H2('Quiz Analytics')

def display_quiz():
    layout = html.Div([
        nav,
        header,
    ])
    return layout