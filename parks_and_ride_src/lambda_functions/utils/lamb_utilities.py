import boto3
import json
from pprint import pprint


def read_file_from_bucket(bucket_name, file_name):
    s3 = boto3.client("s3")
    
    try: 
        content_object = s3.get_object(Bucket=bucket_name, Key=file_name)
        return content_object['Body'] if "Body" in content_object else None
    
    except Exception as e:
        raise e


def write_file_to_s3(bucket_name, s3_path, context):
    s3 = boto3.resource("s3")
    try:
        json_context = json.dumps(context)
        # lambda_path = f"/tmp/{file_name}"
        s3.Bucket(bucket_name).put_object(Key=s3_path, Body=json_context)
        return bucket_name, s3_path
    except Exception as e:
        raise e 


def determine_file_type(file_name):
    return file_name.split(".")[-1]


def retrieve_values(s3_record, *args):
    record = s3_record
    for key in args:
        if key in record:
            record = record[key]
        else: 
            return None, key

    return record


def retrieve_record(event): 
    record = event.get("Records")
    return record[0] if record else None


def validate_attributes(**kwargs):
    invalid_attrs = [
        ValueError(f"Error while retrieving attribute: '{attr_name}' --- Key Nonexistent: '{record[-1]}'") for attr_name, record in kwargs.items() if isinstance(record, tuple)
    ]
    if invalid_attrs:
        raise ValueError(
            f"Processing following attribute errors: {invalid_attrs}. Please check output s3 event notification."
        )

def load_json(json_body):
    return json.load(json_body)

