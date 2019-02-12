#Zbiór bibliotek
import pydicom
from catalog import Catalog, Status
import time
import os
import shutil
import datetime
from ui import UI
#Klasa kontroler modalnosci
class Controller():
    """
    Klasa implementująca system zarządzający przebiegiem procesu badania dla modalności PET.
    """
    def find_study(pat_name, pat_surname):    
        """
        Funkcja wykonuje zapytanie C-FIND do Radiology Information System (RIS) które wyszukuje worklisty o zadanych parametrach.
        
        :param pat_name: Imię pacjenta.
        :param pat_surname: Nazwisko pacjenta
        :return: Lista obiektów DICOM opisujących pasujące Studies zwrócona przez RIS.
        """
        list_of_files=[]
        dicom_file= pydicom.dcmread("worklist_rsp.dcm", force=True)
        list_of_files.append(dicom_file)
        UI.communique(list_of_files)
        return list_of_files
   
     
    def mpps_inprogress(identifier):
        """
        Funkcja N-CREATE zmieniająca status na in-progress- czyli badanie jest w trakcie wykonywania.
        
        :param pat_name: Identyfikator.
        """
        pydicom.dcmread("mpps_inprogress.dcm", force=True)
        examination= Catalog.get(identifier)
        #Zapis pliku mpps_discontinued.dcm do bazy danych
        examination.path="C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\mpps_inprogress.dcm"
        #Zmiana statusu w bazie danych
        examination.status=Status.dicom_inprogress
        Catalog.commit()
        return
          
    
    
    def mpps_completed(identifier):
        """
        Funkcja N-CREATE zmieniająca status na completed- oznacza, że badanie zostało zakończone.
        
        :param pat_name: Identyfikator.
        """
        pydicom.dcmread("mpps_completed.dcm", force=True)
        examination= Catalog.get(identifier)
        #Zapis pliku mpps_discontinued.dcm do bazy danych
        examination.path="C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\mpps_completed.dcm"
        #Zmiana statusu w bazie danych
        examination.status=Status.dicom_completed
        Catalog.commit()
        return
      
        
    def mpps_discontinued(identifier):
        """
        Funkcja N-CREATE zmieniająca status na discontinued- oznacza, ze badanie zostalo anulowane.
        
        :param pat_name: Identyfikator.
        """
        pydicom.dcmread("mpps_discontinued.dcm", force=True)
        examination= Catalog.get(identifier)
        #Zapis pliku mpps_discontinued.dcm do bazy danych
        examination.path="C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\mpps_discontinued.dcm"
        #Zmiana statusu w bazie danych
        examination.status=Status.failed
        UI.communique("The test failed")
        Catalog.commit()
        return
    
    def save_final_data(identifier,file_path_cluster):
        """
        Metoda savefinal_data  obsługuje funkcję C-STORE pozwalającą na wysłanie obrazów z kontrolera modalnosci do serwera np. PACS.
     
        :param pat_name: Identyfikator.
        """
        
        final_image_controller = "C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\controller\\"
        final_file=shutil.copy(file_path_cluster,final_image_controller)
        examination= Catalog.get(identifier)
        #Zapis pliku do bazy danych
        examination.final_image=final_file
        #Zmiana statusu w bazie danych
        examination.status=Status.procedure_completed
        Catalog.commit()
        UI.communique("Final data are saved")
        return               

    
    def build_final_image(identifier, path2):
        """
        Metoda build_final_image odpowiedzialna jest za budowanie końcowego obrazu oraz deanonimizacje 
        
        :param pat_name: Identyfikator.
        """
        cluster_path='C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\cluster\\'
        final_file_cluster_path = os.path.join( cluster_path, str(identifier)+"_final")
        os.rename(path2,final_file_cluster_path)
        examination = Catalog.get(identifier)
        #Zmiana statusu w bazie danych
        examination.status=Status.build_final_image
        Catalog.commit()
        UI.communique("Final image construction in progress")
        return final_file_cluster_path


class Scanner():
        """
        Klasa implementująca funkcje związane z komunikacją ze skanerem         
        """
    
    def scan(identifier):
        """
        Funkcja komunikuje się ze skanerem PET wykorzystując dedykowany niskopoziomowy protokół. Wysyła polecenie rozpoczęcia badania wraz z plikiem DICOM opisującym przeprowadzaną procedurę.
        
        :param pat_name: Identyfikator.
        """
        
        examination = Catalog.get(identifier)
        #Zmiana statusu w bazie danych
        examination.status=Status.scanning
        Catalog.commit()
        UI.communique("Scanning patient")
        return   
        
    def scan_status(identifier):
        """
        Funkcja komunikuje się ze skanerem PET i sprawdza status wykonywanej procedury. Gdy skan zostaje ukończony, funkcja aktualizuje status badania w systemie.
        
        :param pat_name: Identyfikator.
        """
        examination = Catalog.get(identifier)
        #Zmiana statusu w bazie danych
        examination.status=Status.finished_scanning
        Catalog.commit()
        UI.communique("The Scan was executed")
        return  

    def send_scan_results(identifier):
        """
        Wysłanie danych ze skanera PET do kontrolera modalnosci. Gdy dane zostaną wysłane funkcja zmienia status badania w systemie.                 
        
        :param pat_name: Identyfikator.
        """
        
        scanner_pet_path = "C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\scanner\\"
        controller_path = "C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\controller\\"
        file_scanner_path = os.path.join( scanner_pet_path, str(identifier))
        file_controller_path=shutil.copy(file_scanner_path,controller_path)
        examination = Catalog.get(identifier)
        #Zapis pliku do bazy danych
        examination.raw_data_file=file_controller_path
        #Zmiana statusu w bazie danych
        examination.status=Status.send_raw_data
        Catalog.commit()
        UI.communique("The results were sent to the controller")
        return file_controller_path
         

class Cluster():
        """
        Klasa implementująca komunikację pomiędzy klastrem obliczeniowym, a kontrolerem modalnosci                 
        
        """
    
    
    def send_input_data(identifier, path):
        """
        Metoda odpowiedzialna za wysyłanie wejsciowych danych z kontrolera modalnosci do klastra
                
        :param pat_name: Identyfikator.
        """
        
        cluster_path = "C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\cluster"
        file_cluster_path=shutil.copy(path,cluster_path)
        examination = Catalog.get(identifier)
        #Zmiana statusu w bazie danych
        examination.status=Status.reco_data_ready
        Catalog.commit()
        UI.communique("Downloading input data for reconstruction")
        return file_cluster_path

 
    def register(identifier):
        """
        Metoda odpowiedzialna za komunikacje z klastrem obliczeniowym. Zarejestrowanie rekonstrukcji obrazu medycznego
                
        :param pat_name: Identyfikator.
        """
        #Generowanie identyfikatora zadania na klastrze i zapis do bazy danych
        examination = Catalog.get(identifier)
        #Zmiana statusu w bazie danych
        examination.status=Status.reco_registered
        Catalog.commit()
        UI.communique("Reconstruction registered")
        return 


    def start_reconstruction(identifier):
        """
        Metoda ustawiająca dane konkretnego id do systemu kolejkowego w celu rekonstrukcji danych
                
        :param pat_name: Identyfikator.
        """
        
        examination = Catalog.get(identifier)
        #Zmiana statusu w bazie danych
        examination.status=Status.reco_queued
        Catalog.commit()
        UI.communique("Reconstruction queued")
        return 
    

    def status(identifier):
        """
        Metoda aktualizująca status w bazie danych po rekonstrukcji danych
                
        :param pat_name: Identyfikator.
        """
        
        examination = Catalog.get(identifier)
        #Zmiana statusu w bazie danych
        examination.status=Status.reco_finished        
        Catalog.commit()
        return 


    def anonymisation(identifier):
        """
        Metoda implementująca anonimizację danych medycznych 
        :param pat_name: Identyfikator.
        """

        examination = Catalog.get(identifier)
        #Zmiana statusu w bazie danych
        examination.status=Status.finished_anonymisation
        Catalog.commit()
        return
    
    
    def get_output_data(identifier, file_path_cluster):
        """
        Metoda odpowiedzialna za wysłanie wyjsciowych plików z klastra obliczeniowego do kontrolera modalnosci 

        :param pat_name: Identyfikator.
        """
        final_image_controller = "C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\controller\\"
        shutil.copy(file_path_cluster,final_image_controller)
        examination = Catalog.get(identifier)
        #Zmiana statusu w bazie danych
        examination.status=Status.send_final_data
        Catalog.commit()
        UI.communique("The results have been sent")
        return 

   
def run():
    """
    Rdzen mechanizmu
    
    """
    #Zapytanie przez UI personel medyczny w formie imienia i nazwiska pacjenta
    name, surname=UI.query()
    #Na UI zwracana jest lista badan pacjentow o podanym imieniu i nazwisku
    list_of_examinations=Controller.find_study(name,surname)
    #Personel medyczny wybiera, dla ktorego pacjenta przygotowywany bedzie protokol
    number=UI.do_study(list_of_examinations)
    
    #Pętla po elementach w scheduled procedure step sequence
    i=0
    for step in list_of_examinations[number].ScheduledProcedureStepSequence:
        if step.ScheduledStationAETitle=='FILMDIGITIZE':
            break
        i=+1
    if i>len(list_of_examinations[number].ScheduledProcedureStepSequence):
        UI.communique("AE title not found")
        return
        
    
    
    # Tworzenie obiektu badanie, ktory bedzie dodany do bazy danych:
    examination_id= Catalog.newstudy(patient_name=str(list_of_examinations[number].PatientName),
                              patient_id=list_of_examinations[number].PatientID,
                              patients_sex=list_of_examinations[number].PatientSex,
                              start_date=datetime.datetime.strptime(list_of_examinations[number].ScheduledProcedureStepSequence[i].ScheduledProcedureStepStartDate,'%Y%m%d'),
                              end_date=datetime.datetime.strptime(list_of_examinations[number].ScheduledProcedureStepSequence[i].ScheduledProcedureStepEndDate,'%Y%m%d'),
                              aetitle=list_of_examinations[number].ScheduledProcedureStepSequence[i].ScheduledStationAETitle,
                              accession_number=list_of_examinations[number].AccessionNumber,
                              requested_procedure_id=list_of_examinations[number].RequestedProcedureID,
                              final_image=None,
                              raw_data_file=None,
                              path_mpps=None)
    
#Pętla przetwarza badanie, aż nie zakończy się poprawnie lub zgłosi błąd. Dla każdego stanu wykorzystywana jest odpowiednia funkcja, która taki stan obsługuje.
    loop=True   
    while(loop):
        examination=Catalog.get(examination_id)
        if examination.status==Status.new:
    #Przesłanie n-create oraz zmiana statusu na inprogress
            Controller.mpps_inprogress(examination_id)        
        elif examination.status==Status.dicom_inprogress:
            #Wykonywany jest skan pacjenta
            Scanner.scan(examination_id)
        elif examination.status==Status.scanning:
            #Sprawdzany jest status skanowania
            Scanner.scan_status(examination_id)
        elif examination.status==Status.finished_scanning:
            #Wysyłanie surowych danych ze skanera do kontrolera modalnosci
            path_controller=Scanner.send_scan_results(examination_id)            
        elif examination.status==Status.send_raw_data:
            #Następuje anonimizacja danych
            Cluster.anonymisation(examination_id)            
        elif examination.status==Status.finished_anonymisation:   
            #Przez API rejestrowane są nowe zadania obliczeniowe. Klaster ma za zadanie zweryfikować nas, że podaje nam identyfikator zadania i czeka na wrzucenie danych
            Cluster.register(examination_id)
        elif examination.status==Status.reco_registered:
            #Przesylane sa dane wejsciowe z kontrolera modalnosci na klaster obliczeniowy
            path_file_cluster=Cluster.send_input_data(examination_id, path_controller)
        elif examination.status==Status.reco_data_ready:
            #Rekonstrukcja obrazu oczekuje w systemie kolejkowym na klastrze obliczeniowym na przydzielenie zasobow obliczeniowych
            Cluster.start_reconstruction(examination_id)
        elif examination.status==Status.reco_queued or examination.status == Status.reco_running:    
            # Po ukonczeniu rekonstrukcji nastepuje aktualizacja statusu w bazie danych
            Cluster.status(examination_id)
        elif examination.status==Status.reco_finished:
            #Wysłanie danych z klastra do kontrolera modalnosci
            Cluster.get_output_data(examination_id, path_file_cluster)
        elif examination.status==Status.send_final_data:
            # Budowanie koncowego obrazu na klastrze obliczeniowym
            final_file_cluster=Controller.build_final_image(examination_id,path_file_cluster )   
        elif examination.status==Status.build_final_image:    
            #Wysłanie danych z klastra do kontrolera modalnosci
            Controller.save_final_data(examination_id,final_file_cluster)
        elif examination.status==Status.procedure_completed:
            #Wysłanie n-create ze statusem completed, co w rzeczywistosci oznacza ukonczenie badania
            Controller.mpps_completed(examination_id)    
        elif examination.status==Status.dicom_completed:
            #Zakończenie pętli
            loop=False
        elif examination.status==Status.failed:
            # Wysłanie n-create ze statusem discontinued, co oznacza, że badanie zostało anulowane
            Controller.mpps_discontinued(examination_id)
            #Zakończenie pętli
            loop=False
        time.sleep(3)
    return
#Uruchomienie funkcji run
run()    