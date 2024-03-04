# Import Packages and other files for app
import index
from app import app, server  # NEED THE IMPORT SERVER FOR RENDER
from dash import dcc, html, clientside_callback, State
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import warnings
from datetime import date
import coordinates
import globe
import weather
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import dash_extensions as de
import os
from flask import send_from_directory

today = date.today()
warnings.simplefilter(action='ignore', category=FutureWarning)

GITHUB = 'https://github.com/joegriff19'
LINKEDIN = 'https://www.linkedin.com/in/joseph-m-griffin/'
# LOTTIE = 'https://assets5.lottiefiles.com/packages/lf20_GoeyCV7pi2.json'
# LOTTIE = 'https://assets2.lottiefiles.com/packages/lf20_mDnmhAgZkb.json'
options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# Index Page Layout
colors = {
    # 'background': '#ffffff',
    # 'text': '#0000CD'
    'text': '#ffffff',

}

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)
lon_deg = -50

# define sidebar layout
app.layout = html.Div([
    dcc.Location(id="url"),
    content,
])


op_lat_lon_str = weather.get_lat_lon(coordinates.op_geojson)
chi_lat_lon_str = weather.get_lat_lon(coordinates.chicago_geojson)
ber_lat_lon_str = weather.get_lat_lon(coordinates.ber_geojson)
stl_lat_lon_str = weather.get_lat_lon(coordinates.stl_geojson)
mad_lat_lon_str = weather.get_lat_lon(coordinates.madrid_geojson)
dbq_lat_lon_str = weather.get_lat_lon(coordinates.dubuque_geojson)

# index page layout
index_layout = html.Div(
    children=[
        html.Header(
            children=[
                # html.Div(x),
                html.Div(children="Where in the world", className="wg"),
                html.Div(children="are the Griffins?", className="wg"),
                html.Br(),
                dcc.Interval(id='update-rotation', interval=500, n_intervals=0),
                html.Div(children=[
                    html.Div(de.Lottie(options=options, width="10vh", height="10vh", url="/loader", speed=1,
                                       isClickToPauseDisabled=True),
                             style={'display': 'inline-block', "position": "absolute", "top": "95px"}),
                    html.Div(dcc.Graph(
                        id='rotating-globe',
                        config={
                            'displayModeBar': False,
                            'scrollZoom': False,
                            'doubleClick': False,
                        },
                        style={
                            'height': '30vh',
                        }
                    ), style={'width': '30vh', 'display': 'inline-block'}
                    ),
                ]),
            ],
            style={
                'textAlign': 'center',
                'justify': 'center',
                'color': 'white',
                "padding": "0px",
                "margin": "0px"
            }
        ),
        html.Br(),
        html.Br(),
        html.Div([
            html.Div([
                html.Img(src=app.get_asset_url('mom_dad.png'), style={'height': '15vh'}),
                html.Div('📍 Oak Park'),
                html.Div(id="op_weather", children=[], className='weather'),
                html.Br(),
                html.Br(),
            # ], style={'width': '20%', 'display': 'inline-block'}),
            ], style={'color': 'white'}),

            html.Div([
                html.Img(src=app.get_asset_url('joe_circle.png'), style={'height': '15vh'}),
                html.Div('📍 Berlin'),
                html.Div(id="ber_weather", children=[], className='weather'),
                html.Br(),
                html.Br(),
            # ], style={'width': '20%', 'display': 'inline-block'}),
            ], style={'color': 'white'}),

        ]),
        html.Div([
            html.Div([
                html.Img(src=app.get_asset_url('peter.png'), style={'height': '15vh'}),
                html.Div('📍 Chicago'),
                html.Div(id="chi_weather", children=[], className='weather'),
                html.Br(),
                html.Br(),
            # ], style={'width': '20%', 'display': 'inline-block'}),
            ], style={'color': 'white'}),

            html.Div([
                html.Img(src=app.get_asset_url('molly.png'), style={'height': '15vh'}),
                html.Div('📍 Madrid'),
                html.Div(id="mad_weather", children=[], className='weather'),
                html.Br(),
                html.Br(),
            # ], style={'width': '20%', 'display': 'inline-block'}),
            ], style={'color': 'white'}),

        ]),
        html.Div([
            html.Div([
                html.Img(src=app.get_asset_url('libby2.png'), style={'height': '15vh'}),
                html.Div('📍 St. Louis'),
                html.Div(id="stl_weather", children=[], className='weather'),
                html.Br(),
                html.Br(),
            # ], style={'width': '20%', 'display': 'inline-block'}),
            ], style={'color': 'white'}),

            html.Div([
                html.Img(src=app.get_asset_url('janet.png'), style={'height': '15vh'}),
                # html.Div('BONUS!'),
                html.Div('📍 Dubuque -- bonus!'),
                html.Div(id="dbq_weather", children=[], className='weather'),
                html.Br(),
                html.Br(),
            # ], style={'width': '20%', 'display': 'inline-block'}),
            ], style={'color': 'white'}),
        ]),

        html.Div(children=[
            dmc.Group(
                children=[
                    dmc.Anchor(
                        children=[DashIconify(
                            icon='line-md:github-loop', width=40, color="#FF69B4")
                        ],
                        href=GITHUB
                    ),
                    dmc.Anchor(
                        children=[
                            DashIconify(
                                icon='ri:linkedin-fill', width=40, color="#FF69B4")
                        ],
                        href=LINKEDIN
                    )
                ], position='center'
            )
            ]),
            html.Br(),
            # html.Div(children="🍻", style={"fontSize": "35px"}),
            html.Br(),
        ], style={'textAlign': 'center',
                  'max-width': '900px',
                  'margin': 'auto',
                  # 'margin-left': '100px', 'margin-right': '100px',
                  'color': 'text',
                  # 'width': '50%',
                  # 'verticalAlign': 'middle'
                  # 'align-items': 'center', 'justify-content': 'center'
                  }
        ),
    # ])


# page callbacks


@server.route("/loader", methods=['GET'])
def serving_lottie_loader():
    directory = os.path.join(os.getcwd(), "assets/lottie")
    return send_from_directory(directory, "plane4.json")


@app.callback(
    Output('rotating-globe', 'figure'),
    [Input('update-rotation', 'n_intervals')]
)
def rotate_globe(_):
    index.lon_deg = index.lon_deg + 1
    x = index.lon_deg
    return globe.fig.update_layout(geo=dict(center_lon=x, projection_rotation_lon=x))


@app.callback(
    Output('page-content', 'children', ),
    [Input('url', 'pathname', )]
)
def render_page_content(pathname):
    if pathname == '/':
        return index_layout
    # If the user tries to reach a different page, return a 404 message
    else:
        return dbc.Container(
            [
                html.H1("404: Page not found", className="text-danger"),
                html.P("Please return to the home page", className="lead"),
                dbc.Button(children='Wandering Griffin Travel Home Page', id='home', href='/')
            ],
            style={
                'textAlign': 'center',
                'justify': 'center',
                "padding": "0px",
                "margin": "0px"
            }
        )


@app.callback(
    Output('op_weather', 'children', ),
    [Input('url', 'pathname', )]
)
def fetch_op_weather(pathname):
    if pathname == '/':
        return weather.update_weather(op_lat_lon_str)


@app.callback(
    Output('dbq_weather', 'children', ),
    [Input('url', 'pathname', )]
)
def fetch_dbq_weather(pathname):
    if pathname == '/':
        return weather.update_weather(dbq_lat_lon_str)


@app.callback(
    Output('chi_weather', 'children', ),
    [Input('url', 'pathname', )]
)
def fetch_chi_weather(pathname):
    if pathname == '/':
        return weather.update_weather(chi_lat_lon_str)


@app.callback(
    Output('mad_weather', 'children', ),
    [Input('url', 'pathname', )]
)
def fetch_mad_weather(pathname):
    if pathname == '/':
        return weather.update_weather(mad_lat_lon_str)


@app.callback(
    Output('stl_weather', 'children', ),
    [Input('url', 'pathname', )]
)
def fetch_stl_weather(pathname):
    if pathname == '/':
        return weather.update_weather(stl_lat_lon_str)


@app.callback(
    Output('ber_weather', 'children', ),
    [Input('url', 'pathname', )]
)
def fetch_ber_weather(pathname):
    if pathname == '/':
        return weather.update_weather(ber_lat_lon_str)

