#SQLAlchemy jest zbiorem narzędzi do pracy z bazami danych i Pythonem.
#Składa się z narzędzi SQL oraz mapowania obiektowo-relacyjnego -ORM.
#Zbior bibliotek
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Enum, create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
import enum
from sqlalchemy import DateTime
from ui import UI
#Połączenie z bazą danych SQLite.
sqlite_db = create_engine('sqlite:///memory', echo=True)

#Kontruktor podstawowej klasy do definiowania innych klas
Base = declarative_base()

#Stworzenie skonfigurowanej klase Sesja
Session = sessionmaker(bind=sqlite_db)
#Tworzenie sesji
session = Session()


class Status(enum.Enum):
    """
    Klasa Status do tworzenia liczbowych zmiennych, w tym przypadku różnych statusów badania
    """
    
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
    

class Study(Base):
    """
    Klasa implementująca kolumny w bazie danych oraz okreslająca ich typ
    """
    
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
    
    def __repr__(self):
        """
        Metoda okreslająca w jaki sposób prezentowane mają być dane
    
        """
        return "<{'%s':('%s','%s', '%s','%s','%s',,'%s','%s','%s','%s','%s','%s','%s')}>" % (self.id,self.patient_name,self.patient_id, self.patients_sex, self.start_date, self.end_date, self.aetitle, self.accession_number, self.requested_procedure_id, self.status, self.final_image, self.raw_data_file,self.path_mpps)

Base.metadata.create_all(sqlite_db)
    
class Catalog:
    """
    Klasa Catalog, w której definiowane są funkcje, dzięki którym można utworzyć nowe badanie, zatwierdzić sesję, pobrać badanie, filtrować wyniki m.in. po statusach, usunać badanie. 
    """
    
    def get(number):
    """
    Metoda odpowiedzialna za pobieranie badania o identyfikatorze id
    """
        return session.query(Study).filter(Study.id==number).one()
    

    def commit():
    """
    Metoda odpowiedzialna za zatwierdzanie sesji
    """
        session.commit()
        

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
    """
    Metoda odpowiedzialna za tworzenie nowego badania
    
    :param patient_name: Imię i nazwisko pacjenta,
    :param patient_id: Numer identyfikacyjny pacjenta,
    :param patients_sex: Płeć,
    :param start_date: Data startu, 
    :param end_date: Data zakończenia, 
    :param aetitle: Tytuł AE,
    :param accession_number: Numer dostępu,
    :param requested_procedure_id: Numer identyfikacyjny procedury,
    :param final_image: Obraz końcowy,
    :param raw_data_file: Surowe dane,
    :param path_mpps: Plik MPPS.
    """

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
  

    def return_all():
        """
        Metoda zwracająca wszystkie rekordy z bazy danych
        
        """
        return session.query(Study).all()

    
    def return_with_status(study_status):
        """
        Metoda zwracająca rekordy w zależnosci od statusu
        
        """
        
        return session.query(Study).filter_by(study_status).all()

    
    def delete_study(number):
        """
        Metoda pozwalająca usuwać rekordy w zaleznosci od wskazanego id
        
        """
        session.query(Study).filter(Study.id==number).delete()
        session.commit()
        UI.comunique("You deleted patient nr ",number)