import os
import sys
import dash
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html


from dash.dependencies import Input, Output
from parks_and_ride.dash_app.dashboard_utils.figure_utils import set_color, update_figure
from parks_and_ride.dash_app.database.connection_details import ConnectionDetails
from parks_and_ride.dash_app.database.database_interaction import (
    LotInformation, DatabaseAccessor, DatabaseConnection
)


MAPBOX_ACCESS_TOKEN = open(os.path.join(os.getcwd(), "mapbox_access_token")).read()


database_accessor = DatabaseAccessor(ConnectionDetails, DatabaseConnection)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
application = app.server

app.layout= html.Div([
    html.Div([
    html.H1("Parks and Ride Dashboard"),
    html.Hr()
    ], style={"text-align": "center"}),
    html.Div([
        html.Div([
        html.H4("Description: "),
        html.Div([
            html.Hr(),
            html.P(
            """
            This is a visualization of the parks and ride dataset. The map below is a display of available lots marked by their respective space. 
            The map is color coded from red to green in increasing order corresponding to the amount of parking spaces available within each lot.
            Hover over each data point to find details pertaining to each lot such as the: coordinates, spaces available, exit information, 
            if the lot is paved, if the lot provides lighting, and who currently runs the lot. 
            """),
            html.Br(),
            html.P("Zoom into multiple points on the map and interact with them to find out more information!")
        ], style={"color": "black", "text-align": "center", "padding-left": "150px", "padding-right": "150px"}),
        ], style={"text-align": "center"})
    ], style={
        'background-color': 
        '#b1aeae', 
        'margin-top': '20px', 
        'border': '2px solid rgb(0, 0, 0)',
        'padding': '20px',
        'border-radius': '10px',
        'margin-left': '85px',
        'margin-right': '85px',
        }),
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(
            id='interval-component',
            interval=900*1000, #15 minutes in milliseconds
            n_intervals=0
    )
])


@app.callback(
    Output('live-update-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def create_figure(n):
    fig = go.Figure()

    fig, model_data = update_figure(fig, database_accessor, LotInformation)
    
    fig.update_layout(
        title="Parks and Ride Map",
        title_font= dict(
            size= 30,
            color= "black"
        ),
        title_x=0.5,
        autosize=True,
        hovermode='closest',
        showlegend=False,
        height=700,
        mapbox=dict(
            accesstoken=MAPBOX_ACCESS_TOKEN,
            bearing=0,
            center=dict(
                lat=model_data.latitude.mean(),
                lon=model_data.longitude.mean()
            ),
            pitch=0,
            zoom=5,
            style='dark'
        ),  
    )
    return fig



if __name__ == "__main__":
    application.run(debug=True, port=8000)