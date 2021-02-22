from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Float
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from utils.lamb_utilities import read_file_from_bucket


Base = declarative_base()


class LotInformation(Base):
    __tablename__ = "lot_information"
    id = Column(Integer, primary_key = True, autoincrement=True)
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
    id = Column(Integer, primary_key=True, autoincrement=True)
    paved = Column(String(10))
    lighting = Column(String(25))

    def __repr__(self):
        return f"<ID={self.id}, FacilityInformation(paved={self.paved}, lighting={self.lighting})>"


class OwnershipInformation(Base):
    __tablename__ = "ownership_information"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ownership = Column(String(100))

    def __repr__(self):
        return f"ID={self.id}, OwnershipInformation(ownership={self.ownership})>"


class DatabaseLoader:
    
    def __init__(self, processed_data: list, connection_details: dict, database_connection):
        self.processed_data = processed_data
        self.database = database_connection(connection_details)

    def establish_session(self):
        Session = sessionmaker()
        Session.configure(bind = self.database.engine)
        return Session()
    
    def session_upload(self):
        try:
            session = self.establish_session()
            self.model_data(session)
        except:
            session.rollback()
            raise

        finally:
            session.close()
        
        return True
    
    def model_data(self, session):

        facility_info = {}
        ownership_info = {}
        for record in self.processed_data:
            facility_tup = tuple([record['paved'], record['lighted']])
            if facility_tup not in facility_info:
                facility_model = FacilityInformation(
                    paved=facility_tup[0], lighting=facility_tup[1]
                )
                session.add(facility_model)
                facility_info[facility_tup] = facility_model            
            
            ownership = record['runby']
            if ownership not in ownership_info:
                ownership_model = OwnershipInformation(
                    ownership=ownership
                )
                session.add(ownership_model)

                ownership_info[ownership] = ownership_model

        session.commit()
        
        lot_information = [
            LotInformation(
                title=record['title'],
                exit_=record['exit'],
                spaces=record['spaces'],
                comments=record['comments'],
                latitude=record['latitude'],
                longitude=record['longitude'],
                facility_info = facility_info[tuple([record['paved'], record['lighted']])],
                ownership_info = ownership_info[record['runby']]
            ) for record in self.processed_data
        ]

        session.add_all(
            lot_information
        )
        session.commit()
        
        return True


class DatabaseConnection:

    def __init__(self, connection_details: dict):
        self.engine = self.create_engine(connection_details)
    
    def create_engine(self, connection_details):
        db_uri = connection_details["db_uri"]
        extra_details = "extra_details" in connection_details
        return create_engine(db_uri, **connection_details['extra_details']) if extra_details  else create_engine(db_uri)


def load_to_database(processed_data, connection_details):
    database_loader = DatabaseLoader(processed_data, connection_details, DatabaseConnection)
    # Base.metadata.create_all(database_loader.database.engine)
    database_loader.session_upload()
    return True






