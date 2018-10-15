#SQLAlchemy is a set of tools for working with databases and Python.
#It consists of SQL tools and ORM– Object Relational Mapper.
#Collection of libraries
from sqlalchemy.orm import sessionmaker
#Importing the Column class and data types in the database (Integer, String, Date)
from sqlalchemy import Enum, create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
import enum
from sqlalchemy import DateTime
#Connecting wih in-memory-only SQLite database
sqlite_db = create_engine('sqlite:///memory', echo=True)
#Base class constructor for defining the rest of classes.
Base = declarative_base()
#Create a configured "Session" class
Session = sessionmaker(bind=sqlite_db)
#Create a Session
session = Session()

# Class for creating enumerated constants, in this case: various status of examination
class Status(enum.Enum):
    new = 1 
    scanning = 2
    finished_scanning = 3
    send_raw_data=4
    reco_registered = 5
    reco_data_ready=6
    reco_queued=7
    reco_running = 8
    reco_finished=9    
    finished_anonymisation=10
    build_final_image=11
    send_final_data=12
    procedure_completed=13
    failed=14

#Class for creating columns and specifing type of columns
class Study(Base):
    __tablename__ = 'Study'
    id = Column(Integer, primary_key=True, unique=True,nullable=False)
    patient_name=Column(String)
    patient_id=Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    aetitle=Column(String)
    status = Column(Enum(Status))
    raw_data_file=Column(String)
    final_image=Column(String)
    path_mpps=Column(String)
#
    def __repr__(self):
        return "<{'%s':('%s','%s', '%s','%s','%s',,'%s','%s','%s','%s')}>" % (self.id,self.patient_name,self.patient_id, self.start_date, self.end_date, self.aetitle, self.status, self.final_image, self.raw_data_file,self.path_mpps)

Base.metadata.create_all(sqlite_db)
    
#Class for defining metods to create new study, commit session, get study.
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
                 final_image,
                 raw_data_file,
                 path_mpps):
        
        new_study_record=Study(patient_name=patient_name,
                               patient_id=patient_id,
                               start_date=start_date, 
                               end_date=end_date, 
                               aetitle=aetitle, 
                               #status='new', jest w skrypt2.py 184 wiersz
                               status=status, 
                               final_image=final_image,
                               raw_data_file=raw_data_file,
                               path_mpps=path_mpps)
        session.add(new_study_record)   
        session.commit()
        return new_study_record.id
  

#Usunąć?
#
#Tak na prawdę zamień te wszystkie na return_* (oprócz return_all) na return_with_status który pobiera parametr status.
##W ten sposób będzie można zrobić: studies = Catalog.get_with_status(Status.new)
##Obecny kod i tak nie działa bo statusy są string-ami a powinny być Enum

    def return_all():
        return session.query(Study).all()
  
    
    def return_discontinued():
        return session.query(Study).filter_by(status='DISCONTINUED').all()
    
    
    def return_completed():
        return session.query(Study).filter_by(status='COMPLETED').all()
    
    
    def return_inprogress():
        return session.query(Study).filter_by(status='INPROGRESS').all()

                
    def delete_study(number):
        session.query(Study).filter(Study.id==number).delete()
        session.commit()
        show=print("You deleted patient nr ",number)
        return(show)