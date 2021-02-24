import os
import sys
import plotly.express as px
sys.path.append(os.path.join(os.getcwd(), "parks_and_ride", "lambda_functions"))

from data_access import access_data


MAPBOX_ACCESS_TOKEN = open(os.path.join(os.getcwd(), "mapbox_access_token")).read()



print(access_data())