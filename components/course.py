#Import libraries and modules
from dash import Dash, dash_table, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from components.navbar import create_navbar

#Read course data and course UI table data
course_data = pd.read_csv('data/course.csv')
course_data['duration'] = pd.to_timedelta(
course_data['duration'])
course_ui_data = pd.read_csv('data/course_ui_table.csv', index_col = [0])

#Calculate statistics for display
passed = course_data['passed'].sum()
failed = course_data['failed'].sum()
unique_learners = course_data['actor.name'].nunique()
in_progress = unique_learners - passed - failed
completion_rate = ((passed + failed) / unique_learners) * 100
pass_rate = np.round((passed / unique_learners)*100,2)
duration_min = course_data['duration'][course_data['duration'] !='0 days 00:00:00'].min().total_seconds() //60
duration_max = course_data['duration'].max().total_seconds() // 60
duration_average = course_data['duration'].mean().total_seconds() // 60

#Name and define page components
nav = create_navbar()
course_title = html.H5('How to Play the Game of Golf')
header = html.H2('Course Analytics')

#Create layout
def display_course():
    layout = html.Div(
        className = 'usage-container',
        children = [
            html.Div(className='header',children=[nav, course_title, header]),
            html.Div(className='intro-container', children=[
                html.P(className='intro-text', children='Course analytics are comprised of all learners, completions, and failures.'),
                html.P(className='course_totals',children=[
                    'Total unique learners: ',unique_learners,
                    '. Passed: ', passed, 
                    '. Failed: ', failed,
                    '. In progress: ', in_progress,
                    '.' 
                    ]),
                html.P(className='course_rates',children=[
                    'Completion Rate: ', completion_rate,
                    '%. Pass Rate: ', pass_rate, 
                    '%.' 
                    ]),
                html.P(className='course_durations',children=[
                    'Durations. Min: ', duration_min,
                    ' minutes. Max: ', duration_max, 
                    ' minutes. Average: ', duration_average,
                    ' minutes.' 
                    ]),                
            ]),
            html.Div([
                dash_table.DataTable(
                    id='table-multicol-sorting',
                    columns=[
                        {"name": i, "id": i} for i in course_ui_data.columns
                    ],
                    style_cell={'font-family':'sans-serif'},
                    page_current = 0,
                    page_size = 20,
                    page_action = 'custom',
                    sort_action="custom",
                    sort_mode="multi",
                    sort_by = [],
                )
            ])
        ]
    )
    return layout