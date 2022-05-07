from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from components.home import display_home
from components.usage import display_usage
from components.course import display_course
from components.quiz import display_quiz
from main import app

server = app.server
app.config.suppress_callback_exceptions = False

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/components/usage':
        return display_usage()
    if pathname == '/components/course':
        return display_course()
    if pathname == '/components/quiz':
        return display_quiz()
    else:
        return display_home()


if __name__ == '__main__':
    app.run_server(debug=True)