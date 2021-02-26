from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Float
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import DatabaseError


Base = declarative_base()


class LotInformation(Base):
    __tablename__ = "lot_information"
    id = Column(Integer, primary_key = True, autoincrement=True, nullable=False)
    title = Column(String(100))
    exit_ = Column(String(10))
    spaces = Column(String(15))
    comments = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    facility_id = Column(Integer, ForeignKey('facility_information.id'))
    facility_info = relationship("FacilityInformation", backref="lot_information")
    owner_id = Column(Integer, ForeignKey('ownership_information.id'))
    ownership_info = relationship("OwnershipInformation", backref="lot_information")

    def __repr__(self):
        return f"<ID={self.id}, LotInformation(title={self.title}, latitude={self.latitude}, longitude={self.longitude}), facility_info={self.facility_info}, ownership_info={self.ownership_info}>"


class FacilityInformation(Base):
    __tablename__ = "facility_information"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    paved = Column(String(10))
    lighting = Column(String(25))

    def __repr__(self):
        return f"<ID={self.id}, FacilityInformation(paved={self.paved}, lighting={self.lighting})>"


class OwnershipInformation(Base):
    __tablename__ = "ownership_information"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    ownership = Column(String(100))

    def __repr__(self):
        return f"ID={self.id}, OwnershipInformation(ownership={self.ownership})>"


class DatabaseConnection:

    def __init__(self, connection_details: dict):
        self.engine = self.create_engine(connection_details)
    
    def create_engine(self, connection_details):
        db_uri = connection_details["db_uri"]
        extra_details = "extra_details" in connection_details
        return create_engine(db_uri, **connection_details['extra_details']) if extra_details  else create_engine(db_uri)

    def create_connection(self):
        self.connection = self.engine.connect()
    
    def close_connection(self):
        self.connection.close()

    def create_session(self):
        Session = sessionmaker()
        Session.configure(bind = self.engine)
        return Session()

class DatabaseInteraction:
    def __init__(self, connection_details: dict, database_connection: DatabaseConnection):
        self.database = database_connection(connection_details)


class DatabaseLoader(DatabaseInteraction):
    
    def __init__(self, processed_data: list, connection_details: dict, database_connection: DatabaseConnection):
        self.processed_data = processed_data
        super().__init__(connection_details, database_connection)

    def session_upload(self):
        session = None
        try:
            session = self.database.create_session()
            self.model_data(session)

        except DatabaseError as e:
            session.rollback()
            raise e

        except Exception as e:
            if session:
                session.rollback()
            raise e

        finally:
            session.close()
            # The ingestion takes place in a lambda function which can executed asynchronously but 
            # the state of function has no bearing on application after finished executing.
            # calling dispose to ensure that all connections are disposed of and closed on database side so
            # as not to stretch resources and have useless open connection compounding with each lambda execution.
            self.database.engine.dispose()

        return True
    
    def model_data(self, session):
        try:
            lot_information = []
            for record in self.processed_data:
                linking_info = {
                    "latitude": record['latitude'],
                    "longitude": record['longitude'],
                    "comments": record['comments']
                }
                lot_record = self.get_or_create(
                        session, 
                        LotInformation,
                        linking_info,           
                        title=record['title'],
                        facility_info=self.get_or_create(session, FacilityInformation, paved=record['paved'], lighting=record['lighted']),
                        ownership_info=self.get_or_create(session, OwnershipInformation, ownership=record['runby']),
                        exit_=record['exit'],
                        spaces=record['spaces'],
                    )
                lot_information.append(lot_record)

            session.commit()
            return lot_information

        except Exception as e:
            raise DatabaseError(f"Error occured while in session with DB. Error: {e}")

    def get_or_create(self, session: object, model: object, appends: dict=None, **kwargs):
        exists = session.query(model.id).filter_by(**kwargs).scalar() is not None
        if exists:
            model = session.query(model).filter_by(**kwargs).first()
        else:
            if appends:
                model = model(**kwargs, **appends)
            else:
                model = model(**kwargs)
        session.add(model)
        return model


class DatabaseAccessor(DatabaseInteraction):

    def __init__(self, connection_details, database_connection):
        super().__init__(connection_details, database_connection)

    def load_data_models(self, model_to_load):
        session = None
        try:
            session = self.database.create_session()
            models = self.load_model(session, model_to_load)
        except Exception as e:
            raise e
        
        finally:
            session.close()

        return models

    def load_model(self, session: object, model: object, query_parameters: dict= None):
        if query_parameters:
            loaded_models = session.query(model).filter_by(**query_parameters).all()
        else:
            loaded_models = session.query(model).all()

        return self.format_models(loaded_models, "facility_info", "ownership_info") if loaded_models else None

    def format_models(self, models, *args):
        bad_strings = ["_sa_instance_state", "id"]
        formatted_models = []
        for model in models:
            work_model = model.__dict__
            if args:
                for submodel in args:
                    submodel_info = getattr(model, submodel).__dict__
                    for key, value in submodel_info.items():
                        if key not in bad_strings:
                            work_model[key] = value
            formatted_models.append(work_model)
        return formatted_models

    def retrieve_inner_model(self, model):
        return model.__dict__


def read_file_from_bucket(bucket_name, file_name):
    s3 = boto3.client("s3")
    
    try: 
        content_object = s3.get_object(Bucket=bucket_name, Key=file_name)
        return content_object['Body'] if "Body" in content_object else None
    
    except Exception as e:
        raise e


def load_to_database(processed_data, connection_details):
    database_loader = DatabaseLoader(processed_data, connection_details, DatabaseConnection)
    # Base.metadata.create_all(database_loader.database.engine)
    database_loader.session_upload()
    return True
