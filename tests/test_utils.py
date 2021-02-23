import pytest
import os

from parks_and_ride.lambda_functions.utils.lamb_utilities import (
    determine_file_type, retrieve_values, retrieve_record, validate_attributes,
    load_json
)


def test_determine_file_type():
    assert "csv" == determine_file_type("test.csv")


def test_retrieve_values():
    test_record = {
        "foo": {
            "bar": "test_value1"
        },
        "fizz": {
            "buzz": "test_value2"
        }
    }

    assert "test_value1"  == retrieve_values(test_record, "foo", "bar")
    assert (None, "buzzes") == retrieve_values(test_record, "fizz", "buzzes")


def test_retrieve_record():
    test_record = {
        "Records": [
            {}
        ]
    }
    assert {} == retrieve_record(test_record)
    assert None == retrieve_record({})


def test_validate_attributes():
    with pytest.raises(ValueError) as e:
        validate_attributes(bucket_name=(None, "buzzes"))


def test_load_json():
    result = {
        "foo": "bar"
    }
    with open(os.path.join("tests", "test_files", "testing_json.json"), "r") as infile:
        assert result == load_json(infile)
