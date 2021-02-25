import pandas as pd


def format_models_for_graph_use(models):
    return pd.DataFrame(models)
    

def access_data(database_accessor, model):
    models = database_accessor.load_data_models(model)
    return format_models_for_graph_use(models)
