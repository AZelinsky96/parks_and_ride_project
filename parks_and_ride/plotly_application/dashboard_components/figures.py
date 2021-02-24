import plotly.graph_objects as go
import os

from dashboard_components.data_access import access_data


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
    print(model_data.columns)
    fig.add_trace(go.Scattermapbox(
        lat=model_data.latitude,
        lon=model_data.longitude,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=8,
            color= list(map(set_color, map(lambda x: int(x), model_data.spaces)))
        ),
        text=[f'Title: {title}<br>Latitude: {lat}<br>Longitude: {lon}<br>Spaces Available: {spaces}' for title, lat, lon, spaces in list(
            zip(model_data.title, model_data.latitude, model_data.longitude, model_data.spaces))],
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
    return fig