#Import libraries and modules
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from components.navbar import create_navbar

#Read usage data
usage_data = pd.read_csv('data/usage.csv')

#Calculate statistics for display
total_learners = usage_data['actor.name'].nunique()
learners_launched = usage_data['launched'].sum()
resumptions = usage_data['resumed'].sum()
single_session_learners = total_learners - resumptions

#Name and define page components
nav = create_navbar()
course_title = html.H5('How to Play the Game of Golf')
header = html.H2('Usage Analytics')
usage_over_time = px.bar(
    usage_data,
    x = 'date',
    y = 'launched',
    title = 'Daily Launches over Time'
)
cumulative_usage_over_time = px.ecdf(
    usage_data,  
    x = "date", 
    y = 'launched',
    ecdfnorm = None,
    # marginal = 'histogram', 
    title = 'Cumulative Launches over Time'
)

#Create layout
def display_usage():
    layout = html.Div(
        className = 'usage-container',
        children = [
            html.Div(className='header',children=[nav, course_title, header]),
            html.Div(className='intro-container',children=[
                html.P(className='intro-text',children='Usage analytics are traffic counts, comprised of learners who enter, exit, and come back to the course.'),
                html.P(className='intro-text',children=[
                    'Total Access: ',total_learners,
                    ' learners. Learners who accessed the course one time: ',
                    single_session_learners,
                    '. Total return trips to the course: ',
                    resumptions,
                    '.' 
                    ]),
            ]),
            html.Div(
                id='daily-usage-container',
                children= dcc.Graph(
                    id = 'daily-usage-graph',
                    figure = usage_over_time
            )),
            html.Div(
                id="cumulative-usage-container",
                children = dcc.Graph(
                    id='cumulative-usage-graph',
                    figure = cumulative_usage_over_time
                )
            )
        ]
    )
    return layout