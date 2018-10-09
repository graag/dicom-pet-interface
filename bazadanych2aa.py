from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc, Enum
from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
#sqlite_db = create_engine('sqlite:///db.sqlite', echo=True)
sqlite_db = create_engine('sqlite:///memory', echo=True)
import enum

# baza dla klas tabel
Base = declarative_base()
Session = sessionmaker(bind=sqlite_db)
session = Session()

class Status(enum.Enum):
    new = 1 
    scanning = 2
    finished_scanning = 3
    przeslanie_raw_data=4
    reconstructing = 5
    finished_reconstruction = 6
    trwa_anonimizacja=8
    finished_anonimization=9
    finished_analysis=10
    budowanie_koncowego_obrazu=11
    wyslanie_koncowych_danych=12
    procedura_zakonczona=13


class Study(Base):
    __tablename__ = 'Study'
    id = Column(Integer, primary_key=True, unique=True,nullable=False)
    patient_name=Column(String)
    patient_id=Column(String)
    start_date = Column(String)
    end_date = Column(String)
    aetitle=Column(String)
    status = Column(Enum(Status))
    raw_data_file=Column(String)
    reconstructed_image=Column(String)


    def __repr__(self):
        return "<{'%s':('%s','%s', '%s','%s','%s',,'%s','%s','%s','%s','%s','%s')}>" % (self.id,self.patient_name,self.patient_id, self.start_date, self.end_date, self.aetitle, self.status, self.reconstructed_image, self.raw_data_file)

Base.metadata.create_all(sqlite_db)
    

class Catalog:
    def get(number):
        return session.query(Study).filter(Study.id==number).one()
    
    
    def commit():
        session.commit()
        
    def newstudy(patient_name,
                 patient_id,
                 start_date, 
                 end_date, 
                 aetitle,
                 status,
                 reconstructed_image,
                 raw_data_file):
        
        new_study_record=Study(patient_name=patient_name,
                               patient_id=patient_id,
                               start_date=start_date, 
                               end_date=end_date, 
                               aetitle=aetitle, 
                               status=status, 
                               reconstructed_image=reconstructed_image,
                               raw_data_file=raw_data_file)
        session.add(new_study_record)   
        session.commit()
        return new_study_record.id
    

    def return_all():
        for instance in session.query(Study).all():
            print(instance)
        return(instance)
  
    
    def return_discontinued():
        for instance in session.query(Study).filter_by(status='DISCONTINUED').all():
            print(instance)
        return(instance)
    
    
    def return_completed():
        for instance in session.query(Study).filter_by(status='COMPLETED').all():
            print(instance)
        return(instance)
    
    
    def return_inprogress():
        for instance in session.query(Study).filter_by(status='INPROGRESS').all():
            print(instance)
        return(instance)

    
    def session_scope(study):
        if not isinstance(study, Catalog):
            raise Exception("Object is not an Catalog instance: %s", type(study))
        session=study.new_session
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
            
                
    def delete_study(number):
        session.query(Study).filter(Study.id==number).delete()
        session.commit()
        show=print("You deleted patient nr ",number)
        return(show)
        
        
    def update_inpro(name):
        session.query(Study).filter(Study.patient_name == name).\
        update({Study.status: "INPROGRESS"}, synchronize_session=False)
        session.commit()
        return print("Zaktualizowano status badania")