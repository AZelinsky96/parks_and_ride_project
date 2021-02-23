import os
import sys
import pytest
import pandas as pd

sys.path.append(
    os.path.join(os.getcwd(), "parks_and_ride", "lambda_functions")
)

from parks_and_ride.lambda_functions.data_acquisition.acquire_data import (
    DataframeDataHandler, determine_data_loader
)


@pytest.fixture
def dataframe_handler():
    return DataframeDataHandler(pd.DataFrame(
        {'col1': [1, 2], 'col2': [3, 4]}
    ))



class TestDataframeDataHandler:

    def test_format_data(self, dataframe_handler):
        dataframe_handler.VERIFIED_COLUMNS = ["col1", "col2"]
        dataframe_handler.COLUMN_TO_DROP = "col2"
        # Transforming the value to a dictionary since there is an issue asserting dataframe 
        # with same value
        assert  {"col1": {0: 1, 1: 2}} == dataframe_handler.format_data().to_dict()

    def validate_column_names_error(self, dataframe_handler):
        dataframe_handler.VERIFIED_COLUMNS = ['col1', 'col2']
        with pytest.raises(ValueError):
            dataframe_handler.validate_column_names(['col1', 'invalid_column'])


def test_determine_data_loader_pass():
    data_loaders = {
        "test_value": True
    }

    assert determine_data_loader("test_value", data_loaders)


def test_determine_data_loader_fail():
    with pytest.raises(KeyError):
        determine_data_loader("test_value", {"foo": False})