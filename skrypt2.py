#Zbiór bibliotek
import pydicom
from bazadanych2aa import Catalog, Study, Status
import time
import argparse
import os
import shutil
import time
import datetime

#Klasa kontroler modalnosci
class controller():
    #Funkcja wykonuje C-FIND, która wyszukuje liste plikow spelniajacych kryterium
    def find_study(pat_name, pat_surname):    
        list_of_files=[]
        dicom_file= pydicom.dcmread("worklist_rsp.dcm", force=True)
        list_of_files.append(dicom_file)
        print(list_of_files)
        return list_of_files
        
        #Funkcja n-create zmieniająca status na in-progress- czyli badanie jest w trakcie wykonywania
    def mpps_inprogress(identifier):
        pydicom.dcmread("mpps_inprogress.dcm", force=True)
        examination= Catalog.get(identifier)
        #Zapis pliku mpps_discontinued.dcm do bazy danych
        examination.path="C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\mpps_inprogress.dcm"
        #Zmiana statusu w bazie danych
        examination.status=Status.dicom_inprogress
        Catalog.commit()
        return
          
    
    #Funkcja n-create zmieniająca status na completed- oznacza, że badanie zostało zakonczone
    def mpps_completed(identifier):
        pydicom.dcmread("mpps_completed.dcm", force=True)
        examination= Catalog.get(identifier)
        #Zapis pliku mpps_discontinued.dcm do bazy danych
        examination.path="C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\mpps_completed.dcm"
        #Zmiana statusu w bazie danych
        examination.status=Status.dicom_completed
        Catalog.commit()
        return
      
        
    #Funkcja n-create zmieniająca status na discontinued- oznacza, ze badanie zostalo anulowane
    def mpps_discontinued(identifier):
        pydicom.dcmread("mpps_discontinued.dcm", force=True)
        examination= Catalog.get(identifier)
        #Zapis pliku mpps_discontinued.dcm do bazy danych
        examination.path="C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\mpps_discontinued.dcm"
        #Zmiana statusu w bazie danych
        examination.status=Status.failed
        print("The test failed")
        Catalog.commit()
        return
    

    #Funkcja C-STORE pozwala na wyslanie obrazow z kontrolera modalnosci do serwera np. PACS        
    def save_final_data(identifier,file_path_cluster):
        final_image_controller = "C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\controller\\"
        final_file=shutil.copy(file_path_cluster,final_image_controller)
        examination= Catalog.get(identifier)
        #Zapis pliku do bazy danych
        examination.final_image=final_file
        #Zmiana statusu w bazie danych
        examination.status=Status.procedure_completed
        Catalog.commit()
        print("Final data are saved")
        return               

   #Budowanie końcowego obrazu oraz deanonimizacja     
    def build_final_image(identifier, path2):
        cluster_path='C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\cluster\\'
        final_file_cluster_path = os.path.join( cluster_path, str(identifier)+"_final")
        os.rename(path2,final_file_cluster_path)
        examination = Catalog.get(identifier)
        #Zmiana statusu w bazie danych
        examination.status=Status.build_final_image
        Catalog.commit()
        print("Final image construction in progress")
        return final_file_cluster_path


#Klasa skaner definiująca funkcje związane z komunikacją ze skanerem 
class scanner():
    #Funkcja komunikuje się ze skanerem PET wykorzystując dedykowany niskopoziomowy protokół. Wysyła polecenie rozpoczęcia badania wraz z plikiem DICOM opisującym przeprowadzaną procedurę.
    def scan(identifier):
        examination = Catalog.get(identifier)
        #Zmiana statusu w bazie danych
        examination.status=Status.scanning
        Catalog.commit()
        print("Scanning patient")
        return   
        
    # Funkcja komunikuje się ze skanerem PET i sprawdza status wykonywanej procedury. Gdy skan zostaje ukończony, funkcja aktualizuje status badania w systemie.
    def scan_status(identifier):
        examination = Catalog.get(identifier)
        #Zmiana statusu w bazie danych
        examination.status=Status.finished_scanning
        Catalog.commit()
        print("The Scan was executed")
        return  

    # Wysłanie danych ze skanera PET do kontrolera modalnosci. Gdy dane zostaną wysłane funkcja zmienia status badania w systemie.                 
    def send_scan_results(identifier):
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
        print("The results were sent to the controller")
        return file_controller_path
         
#Klasa user interface zawiera metody umożliwiające wybór pacjenta lub wybór badania, które ma zostać wykonane
class UI():
    #Funkcja umożliwia użytkownikowi znalezienia pacjenta po imieniu i nazwisku
    def query(argv=None):
        parser = argparse.ArgumentParser(description='There is User Interface. You can find patient or examination. Type in patient name and surname')
        Patient_name= parser.add_argument('-n','--name', help='Please, type in patient name', required=False)
        Patient_surname= parser.add_argument('-s','--surname', help='Please, type in patient surname',required=True)
        args = parser.parse_args()    
        print("Finding examination for:  %s %s" % (args.name, args.surname))   
        with pydicom.dcmread("worklist_query.dcm", force=True) as ds:
            ds.PatientName=args.name +" "+ args.surname
            print(ds)
            return Patient_name,Patient_surname
          
    #Funkcja, która komunikuje się z użytkownikiem, aby ten wybrał, które badanie z listy go interesuje.    
    def do_study(list_of_studies):
        while True:
            try:
                confirmation=int(input("Specify number of examination which you want to commision: "))
                if confirmation<=int(len(list_of_studies)-1):
                    print("Examination data preparation completed")
                    break
                else:
                    print("Incorrect number of examination, try again")
            #Obsługa błędów
            except (ValueError, UnboundLocalError):
                print("You don't type integer, try again")
            except IndexError:
                print("Incorrect number of examination, try again")
        return confirmation
    
    
    def communique(text):
        print(text)

#Klasa: klaster obliczeniowy komunikuje się z kontrolerem
class cluster():
    #Wysyłanie wejsciowych danych z kontrolera modalnosci do klastra
    def send_input_data(identifier, path):
        cluster_path = "C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\cluster"
        file_cluster_path=shutil.copy(path,cluster_path)
        examination = Catalog.get(identifier)
        #Zmiana statusu w bazie danych
        examination.status=Status.reco_data_ready
        Catalog.commit()
        print("Downloading input data for reconstruction")
        return file_cluster_path

    #Funkcja komunikująca się z klastrem obliczeniowym. Zarejestrowanie rekonstrukcji   
    def register(identifier):
        #Generowanie identyfikatora zadania na klastrze i zapis do bazy danych
        examination = Catalog.get(identifier)
        #Zmiana statusu w bazie danych
        examination.status=Status.reco_registered
        Catalog.commit()
        print("Reconstruction registered")
        return 

    #Funkcja, która ustawia dane konkretnego id do systemu kolejkowego w celu rekonstrukcji danych
    def start_reconstruction(identifier):
        examination = Catalog.get(identifier)
        #Zmiana statusu w bazie danych
        examination.status=Status.reco_queued
        Catalog.commit()
        print("Reconstruction queued")
        return 
    
    #Gdy rekonstrukcja jest zakonczona nastepuje aktualizacja statusu w bazie danych
    def status(identifier):
        examination = Catalog.get(identifier)
        #Zmiana statusu w bazie danych
        examination.status=Status.reco_finished        
        Catalog.commit()
        return 

    # Anonimizacja danych medycznych
    def anonymisation(identifier):
        examination = Catalog.get(identifier)
        #Zmiana statusu w bazie danych
        examination.status=Status.finished_anonymisation
        Catalog.commit()
        return
    
    # Wysłanie wyjsciowych plików z klastra do kontrolera
    def get_output_data(identifier, file_path_cluster):
        final_image_controller = "C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\controller\\"
        shutil.copy(file_path_cluster,final_image_controller)
        examination = Catalog.get(identifier)
        #Zmiana statusu w bazie danych
        examination.status=Status.send_final_data
        Catalog.commit()
        print("The results have been sent")
        return 


# Rdzeń mechanizmu     
def run():
    #Zapytanie przez UI personel medyczny w formie imienia i nazwiska pacjenta
    name, surname=UI.query()
    #Na UI zwracana jest lista badan pacjentow o podanym imieniu i nazwisku
    list_of_examinations=controller.find_study(name,surname)
    #Personel medyczny wybiera, dla ktorego pacjenta przygotowywany bedzie protokol
    number=UI.do_study(list_of_examinations)
    
    #Pętla po elementach w scheduled procedure step sequence
    i=0
    for step in list_of_examinations[number].ScheduledProcedureStepSequence:
        if step.ScheduledStationAETitle=='FILMDIGITIZE':
            break
        i=+1
    if i>len(list_of_examinations[number].ScheduledProcedureStepSequence):
        print("AE title not found")
        
    
    
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
            controller.mpps_inprogress(examination_id)        
        elif examination.status==Status.dicom_inprogress:
            #Wykonywany jest skan pacjenta
            scanner.scan(examination_id)
        elif examination.status==Status.scanning:
            #Sprawdzany jest status skanowania
            scanner.scan_status(examination_id)
        elif examination.status==Status.finished_scanning:
            #Wysyłanie surowych danych ze skanera do kontrolera modalnosci
            path_controller=scanner.send_scan_results(examination_id)            
        elif examination.status==Status.send_raw_data:
            #Następuje anonimizacja danych
            cluster.anonymisation(examination_id)            
        elif examination.status==Status.finished_anonymisation:   
            #Przez API rejestrowane są nowe zadania obliczeniowe. Klaster ma za zadanie zweryfikować nas, że podaje nam identyfikator zadania i czeka na wrzucenie danych
            cluster.register(examination_id)
        elif examination.status==Status.reco_registered:
            #Przesylane sa dane wejsciowe z kontrolera modalnosci na klaster obliczeniowy
            path_file_cluster=cluster.send_input_data(examination_id, path_controller)
        elif examination.status==Status.reco_data_ready:
            #Rekonstrukcja obrazu oczekuje w systemie kolejkowym na klastrze obliczeniowym na przydzielenie zasobow obliczeniowych
            cluster.start_reconstruction(examination_id)
        elif examination.status==Status.reco_queued or examination.status == Status.reco_running:    
            # Po ukonczeniu rekonstrukcji nastepuje aktualizacja statusu w bazie danych
            cluster.status(examination_id)
        elif examination.status==Status.reco_finished:
            #Wysłanie danych z klastra do kontrolera modalnosci
            cluster.get_output_data(examination_id, path_file_cluster)
        elif examination.status==Status.send_final_data:
            # Budowanie koncowego obrazu na klastrze obliczeniowym
            final_file_cluster=controller.build_final_image(examination_id,path_file_cluster )   
        elif examination.status==Status.build_final_image:    
            #Wysłanie danych z klastra do kontrolera modalnosci
            controller.save_final_data(examination_id,final_file_cluster)
        elif examination.status==Status.procedure_completed:
            #Wysłanie n-create ze statusem completed, co w rzeczywistosci oznacza ukonczenie badania
            controller.mpps_completed(examination_id)    
        elif examination.status==Status.dicom_completed:
            #Zakończenie pętli
            loop=False
        elif examination.status==Status.failed:
            # Wysłanie n-create ze statusem discontinued, co oznacza, że badanie zostało anulowane
            controller.mpps_discontinued(examination_id)
            #Zakończenie pętli
            loop=False
    return
#Uruchomienie funkcji run
run()    