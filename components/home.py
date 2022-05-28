from dash import html
from components.navbar import create_navbar

nav = create_navbar()
course_title = html.H5('How to Play the Game of Golf')
header = html.H2('Learning Analytics')

def display_home():
    layout = html.Div(
        className = 'usage-container',
        children = [
            html.Div(className='header',
            children = [nav,course_title,header]),
            html.Div(className='intro-container',
            children = [
                html.P(className='intro-text',
                children = ['How to Play the Game of Golf is a sample of online learning developed by the creators of xAPI, a technology that enables online courses to communicate results to a single repository from anywhere on the internet. This Learning Analytics dashboard reads and displays data collected that course in May 2022.']),
                html.P(className='intro-text',
                    children = [
                    'Use the MENU at top right to access usage, course, and quiz results.',
                ]),
                html.P(className='intro-text',
                    children = [
                    'Data refreshed: 5/22/2022',
                ]),
                html.P(className='intro-text',
                    children = [
                    'Earliest record: 5/08/2022',
                ]),
                html.P(className='intro-text',
                    children = [
                    'Latest record: 5/15/2022',
                ]),
                html.Img(id='image-container',src='assets/a-golf-course.png')
            ]),
        ],
    )
    return layout