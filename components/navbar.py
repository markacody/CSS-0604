import dash_bootstrap_components as dbc

def create_navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="Menu",
                children=[
                    dbc.DropdownMenuItem("Home", href='/'),
                    dbc.DropdownMenuItem(divider=True), 
                    dbc.DropdownMenuItem("Usage", href='/components/usage'),
                    dbc.DropdownMenuItem("Course", href='/components/course'),
                    dbc.DropdownMenuItem("Quiz", href='/components/quiz'),
                ],
            ),
        ],
        brand="Play Golf Association (PGA)",
        brand_href="/",
        sticky="top",
        color="dark",
        dark=True,
    )
    return navbar