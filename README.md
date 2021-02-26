# Welcome to Parks and Ride Project


## Description:
    This is a multipart application that deals with engineering the data, as well as serving the data to consumer in the form of a mapped dashboard. The data is sourced via a series of lambda function triggered by s3 upload events. You can find design diagrams located within the design and flows folder. When a supported file (i.e. csv) is uploaded to the s3 bucket, this triggers a lambda function to read and process the file into an uniform format. This formatted data is uploaded back to an s3 bucket which in turns triggers another function to build the data models and upload the data to an RDS database. 

    Once the data is uploaded to the database, it is instantly available to the consumer facing dashboard. The dashboard will ping the database every 15 minutes to search for more data to be added to the display. The display is built out as a series of markers overlayed on a roadmap. The markers are positioned according to their latitude and longitude. The markers are color coded from red to green according to the number of spaces available. A marker is colored red if there are few spaces, colored yellow if there is a moderate amount of spaces, and colored green if there are plenty of spaces. If you hover over each individual marker, you will find information pertaining to each unique mark. 


## Prerequisites:
    To make use of this application and run it on your local you will need the following: 
    1. A mapbox token.
    2. A connection_details.py file: This file contains a dictionary of connection details to be utilized by the sqlalchemy orm when initializing an engine object
    
    The application is packaged via poetry to be run on a local environment. Follow the steps below to configure the env.

    1. Install poetry
    2. Within the project directory on same level as .toml file run: poetry install
    3. When trying to run the application run: poetry run python<version> application.py

## How to run Tests:

    Make sure that you followed the steps above to install poetry and intialise the environment. To run the tests, run the run_test.sh shell script via bash.

## Where to find deployed app:
    The deployed application can be found here -> [Parks and Ride Dashboard](http://parksandridedashboard-env.eba-etvkgn2c.us-east-1.elasticbeanstalk.com/)


TODO: Find better deployment methods for lambda functions. (Docker?? Ansible??)

TODO: Expand data_access_layer to include more data sources(json, xml, excel, etc.)
