#Import libraries and modules
from dash import Dash, dash_table, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from components.navbar import create_navbar
import humanize
from humanize.time import precisedelta

#Read course data and course UI table data
course_data = pd.read_csv('data/course.csv')
course_data['duration'] = pd.to_timedelta(
course_data['duration'])
course_ui_data = pd.read_csv('data/course_ui_table.csv', index_col = [0])
durations = course_data.pivot_table(values=['duration'], index='actor.name', aggfunc={'duration':np.max})

#Calculate statistics for display
passed = course_data['passed'].sum()
failed = course_data['failed'].sum()
unique_learners = course_data['actor.name'].nunique()
in_progress = unique_learners - passed - failed
completion_rate = ((passed + failed) / unique_learners) * 100
pass_rate = np.round((passed / unique_learners)*100,2)
duration_min = durations.min().apply(humanize.naturaldelta)[0]
duration_max = durations.max().apply(humanize.naturaldelta)[0]
duration_average = durations.mean().apply(humanize.naturaldelta)[0]

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
                html.P(className='intro-text', children='Course analytics are comprised of all learners, completions, and failures. Results range from 5/8 through 5/15/2022.'),
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
                    '. Max: ', duration_max, 
                    '. Average: ', duration_average,
                    '.' 
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