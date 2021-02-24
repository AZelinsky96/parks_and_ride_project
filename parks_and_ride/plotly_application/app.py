import os
import sys
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
sys.path.append(os.path.join(os.getcwd(), "parks_and_ride", "lambda_functions"))

from data_access import access_data


MAPBOX_ACCESS_TOKEN = open(os.path.join(os.getcwd(), "mapbox_access_token")).read()


def set_color(x):

    if(x < 100):
        return "red"
    elif(x >= 100 | x <= 400):
        return "yellow"
    elif(x > 400):
        return "green"
    else:
        return "blue"


def update_figure(fig):
    model_data = access_data()
    fig.add_trace(go.Scattermapbox(
        lat=model_data.latitude,
        lon=model_data.longitude,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=8,
            color= list(map(set_color, map(lambda x: int(x), model_data.spaces)))
        ),
        text=model_data.title,
        hoverinfo='text'
    ))

    return fig, model_data


def create_figure():
    fig = go.Figure()


    fig, model_data = update_figure(fig)
    
    fig.update_layout(
        title='Parks and Ride Lot Locations',
        autosize=True,
        hovermode='closest',
        showlegend=False,
        mapbox=dict(
            accesstoken=MAPBOX_ACCESS_TOKEN,
            bearing=0,
            center=dict(
                lat=model_data.latitude.mean(),
                lon=model_data.longitude.mean()
            ),
            pitch=0,
            zoom=5,
            style='light'
        ),  
    )
    fig.show()


create_figure()