import os
import sys
import pandas as pd

sys.path.append(os.path.join(os.getcwd(), "parks_and_ride", "lambda_functions"))

from data_modelling.connection_details import ConnectionDetails
from data_modelling.database_interaction import (
    LotInformation, DatabaseAccessor, DatabaseConnection
)

def format_models_for_graph_use(models):
    return pd.DataFrame(models)
    

def access_data():
    database_accessor = DatabaseAccessor(ConnectionDetails, DatabaseConnection)
    models = database_accessor.load_data_models(LotInformation)
    return format_models_for_graph_use(models)
