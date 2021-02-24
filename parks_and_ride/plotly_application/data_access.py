from data_modelling.database_interaction import (
    LotInformation, DatabaseAccessor, DatabaseConnection
)
from data_modelling.connection_details import ConnectionDetails


def access_data():
    database_accessor = DatabaseAccessor(ConnectionDetails, DatabaseConnection)
    return database_accessor.load_data_models(LotInformation)
