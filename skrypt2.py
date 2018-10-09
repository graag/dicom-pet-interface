import pydicom
#import logging
from bazadanych2aa import Catalog, Study, Status
import time
import argparse
import os
import shutil

#logging.debug('Informacje wspomagające debugowanie')
#logging.info('Komunikat informacyjny')
#logging.warning('Ostrzeżenie:nie odnaleziono pliku konfiguracyjnego %s', 'server.conf')
#logging.error('Wystąpił błąd')
#logging.critical('Krytyczny błąd -- zakończenie działania')
##def f():
##    try:    1/0
##    except: logging.exception('Wykryto problem')
##
##f()
#logger = logging.Logger('script')
#stream_logger = logging.StreamHandler()
#formatter = logging.Formatter('%(levelname).1s: %(message)s')
#stream_logger.setFormatter(formatter)
#logger.addHandler(stream_logger)
#logger.setLevel(logging.ERROR)

class UI():
    def zapytanie(argv=None):
        parser = argparse.ArgumentParser(description='W interfejscie UI mozesz wyszukać pacjenta badz badanie. Prosze wpisac imie i nazwisko pacjenta')
        Imie_pacjenta= parser.add_argument('-i','--imie', help='Podaj imie pacjenta', required=False)
        Nazwisko_pacjenta= parser.add_argument('-n','--nazwisko', help='Podaj nazwisko pacjenta',required=True)
        args = parser.parse_args()    
        komunikat=print("Wyszukujemy badania dla:  %s %s" % (args.imie, args.nazwisko))   
        #Wpisanie parametrów z UI do pustej worklisty
        with pydicom.dcmread("worklistquery2usuwanie_errorow5_138.dcm", force=True) as ds:
            ds.PatientName=args.imie +" "+ args.nazwisko
            lista_z_wypelnieniem=print(ds)
        return Imie_pacjenta,Nazwisko_pacjenta, komunikat, lista_z_wypelnieniem
          
    
    def zrob_badanie():
        #ma pobierac parametr ktory oznacza liczbe
        #print lista z wypelnieniem
        potwierdzenie=int(input("Podaj nr badania, które chcesz wykonać z listy: np. 0 "))
        if potwierdzenie==0:
            wys=print("Zakończono sporządzanie danych do badania")
        return potwierdzenie
       

class controller():
    def znajdz_badanie():    
        #wlmRsp0009.dcm jest z C:\Users\Anna\Documents\DVTk\Modality Emulator\Data\Worklist\WLM RSP\20180830132453
        lista_zplikow=[]
        dsa= pydicom.dcmread("wlmRsp0009.dcm", force=True)
        lista_zplikow.append(dsa)
        print(lista_zplikow)
        return lista_zplikow
        
        
    def pobierz_liste_badan():
        ncreate=pydicom.dcmread("mpps-inprogress1_1605_128_ref138_2.dcm", force=True)
        return
          
    
    def status():
        time.sleep(1)
        wydruk=print("Sporządzono protokół")
        return 
        
        
    def zapisz_koncowe_dane(identyfikator):
        time.sleep(1)
        badanie = Catalog.get(identyfikator)
        badanie.status=Status.procedura_zakonczona
        Catalog.commit()
        print("Zapisano koncowe dane")
        return               

 
class scanner():
    def scan(identyfikator):
        badanie = Catalog.get(identyfikator)
        badanie.status=Status.scanning
        Catalog.commit()
        print("Trwa skanowanie pacjenta")
        return  
        
    
    def scan_status(identyfikator):
        badanie = Catalog.get(identyfikator)
        badanie.status=Status.finished_scanning
        Catalog.commit()
        time.sleep(1)
        print("Skan został wykonany")
        return 

                     
    def sent_scan_results(identyfikator):
        time.sleep(1)
        badanie = Catalog.get(identyfikator)
        badanie.status=Status.przeslanie_raw_data
        Catalog.commit()
        source2 = "C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\scanner\\id1.jpg"
        destination2 = "C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\controller"
        shutil.copy(source2,destination2)
        infoo=print("Wyniki zostały przesłane do kontrolera")
        rezultat = open('scan.txt', 'w')                                           #(1)
        rezultat.close()
        return rezultat


class cluster():
    def pobieranie_danych_wejsciowych():
        time.sleep(1)
        source3 = "C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\controller\\id1.jpg"
        destination3 = "C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\cluster"
        shutil.copy(source3,destination3)
        print("Pobieranie danych wejsciowych do rekonstrukcji")
        # czytanei pliku z bazy danych
        return

        
    def rekonstrukcja(identyfikator):
        time.sleep(1)
        badanie = Catalog.get(identyfikator)
        badanie.status=Status.reconstructing
        Catalog.commit()
        print("Trwa rekonstrukcja")
        return

         
    def status_rekonstrukcji(identyfikator):
        time.sleep(1)
        badanie = Catalog.get(identyfikator)
        badanie.status=Status.finished_reconstruction
        Catalog.commit()
        return 

        
    def anonimizacja(identyfikator):
        time.sleep(1)
        badanie = Catalog.get(identyfikator)
        badanie.status=Status.trwa_anonimizacja
        Catalog.commit()
        print("Trwa anonimizacja")  
        return
    
    
    def status_anonimizacji(identyfikator):        
        time.sleep(1)
        badanie = Catalog.get(identyfikator)
        badanie.status=Status.finished_anonimization
        Catalog.commit()
        return 
        
    
    def deanonimizacja(identyfikator):
        time.sleep(1)
        badanie = Catalog.get(identyfikator)
        badanie.status=Status.finished_analysis
        Catalog.commit()
        print("Trwa deanonimizacje")
        return

        
    def budowanie_koncowego_obrazu(identyfikator):
        badanie = Catalog.get(identyfikator)
        badanie.status=Status.wyslanie_koncowych_danych
        Catalog.commit()
        os.rename('C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\cluster\\id1.jpg','C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\cluster\\koncowy.jpg') 
        time.sleep(1)
        print("Trwa budowanie koncowego obrazu")
        return


    def wyslanie_danych_po_analizie(identyfikator):
        badanie = Catalog.get(identyfikator)
        badanie.status=Status.budowanie_koncowego_obrazu
        Catalog.commit()
        source4 = "C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\cluster\\koncowy.jpg"
        destination4 = "C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\controller"
        shutil.copy(source4,destination4)
               
        print("Wyniki zostaly przeslane")
        time.sleep(1)
        return

     
def run():
    UI.zapytanie()
    moja_lista_badan=controller.znajdz_badanie()
    liczba=UI.zrob_badanie()
    #Tworzenie obiektu badanie
    badanie_id= Catalog.newstudy(patient_name=str(moja_lista_badan[liczba].PatientName),
                              patient_id=moja_lista_badan[liczba].PatientID,
                              start_date=moja_lista_badan[liczba].ScheduledProcedureStepSequence[0].ScheduledProcedureStepStartDate,
                              end_date=moja_lista_badan[liczba].ScheduledProcedureStepSequence[0].ScheduledProcedureStepEndDate,
                              aetitle=moja_lista_badan[liczba].ScheduledProcedureStepSequence[0].ScheduledStationAETitle,
                              status="new",
                              reconstructed_image=None,
                              raw_data_file=None)
    lista_konkre=controller.pobierz_liste_badan()
    controller.status()    
    cykl=True   
    while(cykl):
        badanie=Catalog.get(badanie_id)
        if badanie.status==Status.new:
            scanner.scan(badanie_id)
            print(badanie.status)
            
        elif badanie.status==Status.scanning:        
            scanner.scan_status(badanie_id)
        elif badanie.status==Status.finished_scanning:
            #Wysyłanie surowych danych ze skanera do kontrolera modalnosci
            scanner.sent_scan_results(badanie_id)            
        elif badanie.status==Status.przeslanie_raw_data:
            cluster.pobieranie_danych_wejsciowych()
            cluster.rekonstrukcja(badanie_id)            
        elif badanie.status==Status.reconstructing:
            cluster.status_rekonstrukcji(badanie_id)            
        elif badanie.status==Status.finished_reconstruction:
            cluster.anonimizacja(badanie_id)            
        elif badanie.status==Status.trwa_anonimizacja:
            cluster.status_anonimizacji(badanie_id)            
        elif badanie.status==Status.finished_anonimization:
            cluster.deanonimizacja(badanie_id)    
        elif badanie.status==Status.finished_analysis:
            cluster.wyslanie_danych_po_analizie(badanie_id)           
        elif badanie.status==Status.budowanie_koncowego_obrazu:
            cluster.budowanie_koncowego_obrazu(badanie_id)            
        elif badanie.status==Status.wyslanie_koncowych_danych:
            controller.zapisz_koncowe_dane(badanie_id)
        elif badanie.status==Status.procedura_zakonczona:
            cykl=False
    return
run()    