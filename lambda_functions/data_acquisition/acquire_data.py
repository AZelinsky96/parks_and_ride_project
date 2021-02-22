import pandas as pd
import numpy as np

from abc import abstractmethod
from utils.lamb_utilities import (
    read_file_from_bucket, retrieve_values,
    retrieve_record, validate_attributes,
    determine_file_type, write_file_to_s3
)


class DataLoader:

    def __init__(self, file_object: object):
        self.file_object = file_object
    
    @abstractmethod
    def load_data(self):
        raise NotImplementedError("load_data is not implemented because it is an abstract method")


    @abstractmethod
    def call_data_handler(self):
        raise NotImplementedError("call_data_handler is not implemented because it is an abstact method")


class CsvDataLoader(DataLoader):
    
    def load_data(self):
        return self.call_data_handler(pd.read_csv(self.file_object))
        

    def call_data_handler(self, raw_data):
        return DataframeDataHandler(raw_data).format_data()


class DataHandler:
    
    def __init__(self, parks_data):
        self.parks_data = parks_data
    
    def format_data(self):
        raise NotImplementedError("format_data is not implemented because it is an abstract method")


class DataframeDataHandler(DataHandler):

    def format_data(self):
        work_parks_data = self.parks_data
        work_parks_data.columns = list(map(lambda x: x.lower().strip().replace(" ", ""), work_parks_data.columns))
        self.validate_column_names(work_parks_data.columns)
        work_parks_data.drop(['location'], axis=1, inplace=True)
        for column in work_parks_data.columns:
            if work_parks_data[column].dtype == "object":
                work_column = work_parks_data[column]
                work_column.replace(np.nan, "None", inplace=True)
                work_parks_data[column] = work_column.apply(lambda x: x.strip().lower().replace(" ", "_"))
        return work_parks_data

    def validate_column_names(self, columns):
        verified_columns = ['title', 'exit', 'runby', 'spaces', 'paved', 'lighted', 'comments', 'latitude', 'longitude', 'location']
        verification_result = [ValueError(f"Invalid Column: {column_value}") for column_value in columns if column_value not in verified_columns]
        if verification_result:
            raise ValueError(f"Invalid Columns Found: {verification_result}. Adjust csv if necessary.")


DATA_LOADERS = {

    "csv": CsvDataLoader
}


def handle_acquisition_setup(event):
    record = retrieve_record(event)
    bucket_name, file_name = retrieve_values(record, "s3", "bucket", "name"), retrieve_values(record, "s3", "object", "key")
    validate_attributes(bucket_name=bucket_name, file_name=file_name)
    streamed_file_object = read_file_from_bucket(str(bucket_name), str(file_name))
    file_type = determine_file_type(file_name)
    return file_type, streamed_file_object


def determine_data_loader(file_type):
    try:
        return DATA_LOADERS[file_type]
    
    except KeyError:
        raise KeyError(f"Unsupported File Type: {file_type}")
    
    except Exception as e:
        raise e


def load_and_format_data(data_loader, streamed_file_object):
    data_loader_object = data_loader(streamed_file_object)
    return  data_loader_object.load_data()


def acquire_data(file_type, streamed_file_object):
    data_loader = determine_data_loader(file_type)
    return load_and_format_data(data_loader, streamed_file_object)


def output_data_to_s3(bucket_name, folder, output_data, event):
    file_value = retrieve_values(retrieve_record(event), "s3", "object", "key").split("/")[-1].split(".")[0]
    file_name = f"{folder}/{file_value.lower()}_processed.json"
    return write_file_to_s3(bucket_name, file_name, output_data)
    
