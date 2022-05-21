import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from components.home import display_home
from components.usage import display_usage
from components.course import display_course, course_ui_data
from components.quiz import display_quiz

app = dash.Dash(__name__,
 suppress_callback_exceptions=False,
 external_stylesheets=[dbc.themes.LUX])
server = app.server
app.config.suppress_callback_exceptions = True

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

@app.callback(
    Output('table-multicol-sorting', "data"),
    Input('table-multicol-sorting', "page_current"),
    Input('table-multicol-sorting', "page_size"),
    Input('table-multicol-sorting', "sort_by"))
def update_table(page_current, page_size, sort_by):
    print(sort_by)
    if len(sort_by):
        dff = course_ui_data.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )
    else:
        # No sort is applied
        dff = course_ui_data

    return dff.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)