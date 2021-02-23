import os
import boto3
import moto
import pytest

from parks_and_ride.lambda_functions.utils.lamb_utilities import (
    determine_file_type, retrieve_values, retrieve_record, validate_attributes,
    load_json, read_file_from_bucket
)


class MyModel(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def save(self):
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.put_object(Bucket='test_bucket', Key=self.name, Body=self.value)


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


@moto.mock_s3
def test_read_file_from_bucket():
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket="test_bucket")

    model_instance = MyModel("coding", "is_awesome")
    model_instance.save()
    assert "is_awesome" == read_file_from_bucket(bucket_name="test_bucket", file_name="coding").read().decode("utf-8")
    


