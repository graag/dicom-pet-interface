#SQLAlchemy jest zbiorem narzędzi do pracy z bazami danych i Pythonem.
#Składa się z narzędzi SQL oraz mapowania obiektowo-relacyjnego -ORM.
#Zbior bibliotek
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Enum, create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
import enum
from sqlalchemy import DateTime

#Połączenie z bazą danych SQLite.
sqlite_db = create_engine('sqlite:///memory', echo=True)

#Kontruktor podstawowej klasy do definiowania innych klas
Base = declarative_base()

#Stworzenie skonfigurowanej klase Sesja
Session = sessionmaker(bind=sqlite_db)
#Tworzenie sesji
session = Session()

# Klasa status do tworzenia liczbowych zmiennych, w tym przypadku różnych statusów badania
class Status(enum.Enum):
    new = 1 
    dicom_inprogress=2
    scanning = 3
    finished_scanning = 4
    send_raw_data=5
    reco_registered = 6
    reco_data_ready=7
    reco_queued=8
    reco_running = 9
    reco_finished=10   
    finished_anonymisation=11
    build_final_image=12
    send_final_data=13
    dicom_completed=14
    procedure_completed=15
    failed=16
    

#Klasa do definiowania kolumn w bazie danych oraz okreslania ich typu
class Study(Base):
    __tablename__ = 'Study'
    id = Column(Integer, primary_key=True, unique=True,nullable=False)
    patient_name=Column(String)
    patient_id=Column(String)
    patients_sex=Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    aetitle=Column(String)
    accession_number=Column(String)
    requested_procedure_id=Column(String)
    status = Column(Enum(Status),default=Status.new)
    raw_data_file=Column(String)
    final_image=Column(String)
    path_mpps=Column(String)
    #Metoda okreslajaca w jaki sposob prezentowane maja byc dane
    def __repr__(self):
        return "<{'%s':('%s','%s', '%s','%s','%s',,'%s','%s','%s','%s','%s','%s','%s')}>" % (self.id,self.patient_name,self.patient_id, self.patients_sex, self.start_date, self.end_date, self.aetitle, self.accession_number, self.requested_procedure_id, self.status, self.final_image, self.raw_data_file,self.path_mpps)

Base.metadata.create_all(sqlite_db)
    
#Klasa Catalog, w której definiowane są funkcje, dzięki którym można utworzyć nowe badanie, zatwierdzić sesję, pobrać badanie, filtrować wyniki m.in. po statusach, usunać badanie. 
class Catalog:
    #Pobieranie badania o id, które jest parametrem
    def get(number):
        return session.query(Study).filter(Study.id==number).one()
    
    #Zatwierdzanie sesji
    def commit():
        session.commit()
        
    #Metoda do tworzenia nowego badania    
    def newstudy(patient_name,
                 patient_id,
                 patients_sex,
                 start_date, 
                 end_date, 
                 aetitle,
                 accession_number,
                 requested_procedure_id,
                 final_image,
                 raw_data_file,
                 path_mpps):
        #Tworzenie nowego rekordu w bazie danych
        new_study_record=Study(patient_name=patient_name,
                               patient_id=patient_id,
                               patients_sex=patients_sex,
                               start_date=start_date, 
                               end_date=end_date, 
                               aetitle=aetitle,
                               accession_number=accession_number,
                               requested_procedure_id=requested_procedure_id,
                               final_image=final_image,
                               raw_data_file=raw_data_file,
                               path_mpps=path_mpps)
        #Dodawanie nowego rekordu do bazy danych
        session.add(new_study_record)   
        #Zatwierdzanie sesji
        session.commit()
        return new_study_record.id
  

    #Metoda zwracajaca wszystkie rekordy z bazy danych
    def return_all():
        return session.query(Study).all()

    #Metoda zwracająca rekordy w zaleznosci od statusu
    def return_with_status(study_status):
        return session.query(Study).filter_by(study_status).all()

    #Metoda pozwalajaca usuwac rekordy w zaleznosci od wskazanego id
    def delete_study(number):
        session.query(Study).filter(Study.id==number).delete()
        session.commit()
        print("You deleted patient nr ",number)