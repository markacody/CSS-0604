#Import librairies and modules
from dash import Dash, dash_table, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from components.navbar import create_navbar
import humanize
import plotly.express as px

#Read quiz data and quiz questions UI table
quiz_data = pd.read_csv('data/quiz.csv')
quiz_data['duration'] = pd.to_timedelta(quiz_data['duration'])
questions_data = pd.read_csv('data/questions_ui_table.csv',index_col=[0])

#Calculate statistics for display
passed = quiz_data['passed'].sum()
failed = quiz_data['failed'].sum()
unique_learners = quiz_data['actor.name'].nunique()
in_progress = unique_learners - passed - failed
completion_rate = ((passed+failed)/unique_learners) * 100
pass_rate = np.round((passed/unique_learners)*100,2)
min_score = quiz_data['result.score.raw'].min()
max_score = quiz_data['result.score.raw'].max()
average_score = np.round(quiz_data['result.score.raw'].mean(),2)
duration_min = humanize.naturaldelta(quiz_data['duration'][quiz_data['duration']!= '0 days 00:00:00'].min())
duration_max = humanize.naturaldelta(quiz_data['duration'].max())
duration_average = humanize.naturaldelta(quiz_data['duration'].mean())

#Name and define page components
nav = create_navbar()
course_title = html.H5('How to Play the Game of Golf')
header = html.H2('Quiz Analytics')
quiz_graph = px.histogram(quiz_data, x = 'result.score.raw')

#Create layout
def display_quiz():
    layout = html.Div(
        className = 'usage-container',
        children = [
            html.Div(className='header',children=[nav, course_title, header]),
            html.Div(className='intro-container', children=[
                html.P(className='intro-text', children='Quiz analytics are comprised of (1) aggregated results, scores, and durations; (2) a distribution of quiz scores, and (3) all questions with total correct and incorrect responses for each one.'),
                html.P(className='quiz_totals',children=[
                    'Total unique learners: ',unique_learners,
                    '. Passed: ', passed, 
                    '. Failed: ', failed,
                    '. In progress: ', in_progress,
                    '.' 
                    ]),
                html.P(className='quiz_rates',children=[
                    'Completion Rate: ', completion_rate,
                    '%. Pass Rate: ', pass_rate, 
                    '%.' 
                    ]),
                html.P(className='quiz_scores',children=[
                    'Scores. Min: ', min_score,
                    '%. Max: ', max_score, 
                    '%. Average: ', average_score,
                    '%.' 
                    ]),
                html.P(className='quiz_durations',children=[
                    'Durations. Min: ', duration_min,
                    '. Max: ', duration_max, 
                    '. Average: ', duration_average,
                    '.' 
                    ]),
                html.H4('Quiz Distribution'),
                html.Div([
                    dcc.Graph(figure = quiz_graph)
                ]),
                html.H4('Quiz Results'),
                html.Div([
                    dbc.Table.from_dataframe(questions_data, striped=True, bordered=True, hover=True)
                ])                 
            ]),
        
    ])
    return layout