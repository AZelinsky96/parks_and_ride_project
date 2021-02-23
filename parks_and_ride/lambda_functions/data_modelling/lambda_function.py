from database_interaction import load_to_database
from utils.lamb_utilities import (
    retrieve_record, retrieve_values, read_file_from_bucket,
    validate_attributes, load_json
)
from connection_details import ConnectionDetails


def load_processed_data(event):
    record = retrieve_record(event)
    bucket_name, file_name = retrieve_values(record, "s3", "bucket", "name"), retrieve_values(record, "s3", "object", "key")
    validate_attributes(bucket_name=bucket_name, file_name=file_name)
    streamed_file_object = read_file_from_bucket(bucket_name, file_name)
    return load_json(streamed_file_object)


def lambda_handler(event, context):
    processed_data = load_processed_data(event)
    load_to_db = load_to_database(processed_data, ConnectionDetails)
    return {
        "IngestionStatus": "Success"
    } if load_to_db else {
        "IngestionStatus": "Faliure"
    }