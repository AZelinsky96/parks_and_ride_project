from acquire_data import (
    handle_acquisition_setup, acquire_data, output_data_to_s3
)


BUCKET_NAME = "parks-and-ride-test"
FOLDER="processed_data"

def lambda_handler(event, context):
    file_type, streamed_file_object = handle_acquisition_setup(event)
    acquired_data = acquire_data(file_type, streamed_file_object)
    bucket_name, file_name = output_data_to_s3(BUCKET_NAME, FOLDER, acquired_data.to_dict(orient="records"), event)
    
    return {
        "bucket_name": bucket_name,
        "file_name": file_name
    }
