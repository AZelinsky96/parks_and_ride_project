import os
import plotly.graph_objects as go

from dashboard_utilities.data_access import access_data


def set_color(x):
    if(x < 50):
        return "red"
    elif x < 150:
        return "yellow"
    elif(x >= 150):
        return "green"
    else:
        return "blue"


def update_figure(fig, database_accessor, model):
    model_data = access_data(database_accessor, model)
    fig.add_trace(go.Scattermapbox(
        lat=model_data.latitude,
        lon=model_data.longitude,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=8,
            color= list(map(set_color, map(lambda x: int(x), model_data.spaces))),
            opacity= 0.7
        ),
        text=[f'''Title: {title}
        <br>Latitude: {lat}<br>Longitude: {lon}<br>Spaces Available: {spaces}
        <br>Exit: {exit_}<br>Lighting: {lighting}
        <br>Paved: {paved}<br>Ownership: {owner}''' for title, lat, lon, spaces, exit_, lighting, paved, owner in list(
            zip(model_data.title, model_data.latitude, model_data.longitude, 
            model_data.spaces, model_data.exit_, model_data.lighting, model_data.paved, model_data.ownership))],
        hoverinfo='text'
    ))

    return fig, model_data
