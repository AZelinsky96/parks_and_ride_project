import dash
import dash_core_components as dcc
import dash_html_components as html


from dashboard_components.figures import create_figure


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def create_app_layout(app):
    fig = create_figure()
    app.layout= html.Div([
        dcc.Graph(figure=fig)
    ])
    return app



if __name__ == "__main__":
    app = create_app_layout(app)
    app.run_server(debug=True)