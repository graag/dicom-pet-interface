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
#
##def f():
##    try:    1/0
##    except: logging.exception('Wykryto problem')
##
##f()
#
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
        ## podaj nr badania ktore chcesz wykonac z listy worklist rsp
        potwierdzenie=input("Czy chcesz wykonać badanie dla tego pacjenta. Jesli tak, wpisz: y, jesli nie, wpisz: n : ")
        
        if potwierdzenie=="y":
            wys=print("Zakończono sporządzanie danych do badania")
        return wys
        
    def display():
        wysw=print("?????????????")
        return wysw
########################################################################################################

class controller():
    def znajdz_badanie():
#wysłanie response c-find -problem z zapisaniem response c-find
# ale gdy bedzie plik, to czy program ma go tylko printować w IU?
#czytanie dcm i print/ wyswietlenie listy na UI:
        
        #wlmRsp0009.dcm jest z C:\Users\Anna\Documents\DVTk\Modality Emulator\Data\Worklist\WLM RSP\20180830132453
        #proponuje wykorzystac to
        lista_zplikow=[]
        dsa= pydicom.dcmread("wlmRsp0009.dcm", force=True)
        lista_zplikow.append(dsa)
        
        print(lista_zplikow)
        return lista_zplikow
        
     #pobierz dane ze skanera
    def pobierz_dane():
#save obrazka
        return 
        
    def pobierz_liste_badan():



        ncreate=pydicom.dcmread("mpps-inprogress1_1605_128_ref138_2.dcm", force=True)
#        ncreate.PatientName="Jan Kowalski"
#        Namepacjenta=ncreate.PatientName
#        Idpacjenta=ncreate.PatientID
#        Datastartu=ncreate.PerformedProcedureStepStartDate
#        Datakonca=ncreate.PerformedProcedureStepEndDate
#        AEtitle=ncreate.PerformedStationAETitle

        #sciezka do pliku
        return
          
    def status():
        time.sleep(1)
        wydruk=print("Sporządzono protokół")
        return 
        
        
    def zapisz_koncowe_dane():
        time.sleep(1)
        print("Zapisano koncowe dane")

        return               
############################################### 
class scanner():
    def scan():
        print("Trwa skanowanie pacjenta")
        return  
        
    def scan_status():
        time.sleep(1)
        return 
                     
    def sent_scan_results():
        time.sleep(1)
        time.sleep(1)

        source2 = "C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\scanner\\id1.jpg"
        destination2 = "C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\controller"
        shutil.copy(source2,destination2)

        infoo=print("Wyniki zostały przesłane do kontrolera")
        
        rezultat = open('scan.txt', 'w')                                           #(1)
        rezultat.close()
        return rezultat
#################################################################
class cluster():
    
    def pobieranie_danych_wejsciowych():
        time.sleep(1)
        source3 = "C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\controller\\id1.jpg"
        destination3 = "C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\cluster"
        shutil.copy(source3,destination3)
        print("Pobieranie danych wejsciowych do rekonstrukcji")
        # czytanei pliku z bazy danych
        return
        
    def rekonstrukcja():
        time.sleep(1)
        print("Trwa rekonstrukcja")
        return
         
    def status_rekonstrukcji():
        time.sleep(1)
        
        return 
        
    def anonimizacja():
        time.sleep(1)
        print("Trwa anonimizacja")
        
        return
        
    def status_anonimizacji():        
        time.sleep(1)
        
        return 
        
    def deanonimizacja():
        time.sleep(1)
        print("Trwa deanonimizacje")

        return
        
    def budowanie_koncowego_obrazu():
        
         
        os.rename('C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\cluster\\id1.jpg','C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\cluster\\koncowy.jpg') 
        
        time.sleep(1)
        print("Trwa budowanie koncowego obrazu")

        return

    def wyslanie_danych():
        source4 = "C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\cluster\\koncowy.jpg"
        destination4 = "C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\controller"
        shutil.copy(source4,destination4)
               
        print("Wyniki zostaly przeslane")
        time.sleep(1)
        return

#####################################################
    
def run():
    #zapytanie UI
    UI.zapytanie()
    #controller.znajdz_badanie()
    moja_lista_badan=controller.znajdz_badanie()
    UI.zrob_badanie()
      
    
    
    #utworz obiekt Badanie
#    badanie= Catalog.newstudy(patient_name=moja_lista_badan[0].PatientName,
#                              patient_id=moja_lista_badan[0].PatientID,
#                              #moja_lista_badan[0].ScheduledProcedureStepStartDate,
#                              #moja_lista_badan[0].PerformedProcedureStepEndDate,
#                              #moja_lista_badan[0].PerformedStationAETitle,
#                              end_date=None,
#                              start_date=None,
#                              aetitle=None,
#                              status=None,
#                              reconstructed_image=None,
#                              raw_data_file=None)
#    
    lista_konkre=controller.pobierz_liste_badan()
    controller.status()
    #if status_dicom=="INPROGRESS":
    #    Catalog.update_inpro(Namepacjenta)
   
    
    cykl=True
    
    while(cykl):
        
        badanie=Study(new_study_record.id)
        
        if badanie.status==Status.new:
            scanner.scan()
        elif badanie.status==Status.scanning:        
            scanner.scan_status()
        elif badanie.status==Status.finished_scanning:
            time.sleep(2)
            print("Skan został wykonany")
            controller.pobierz_dane()
            #wyslij surowe dane ze skanera do kontrolera modalnosci
            scanner.sent_scan_results()
            
        elif badanie.status==Status.przeslanie_raw_data:
            #rekonstrukcja danych
            cluster.pobieranie_danych_wejsciowych()
            cluster.rekonstrukcja()
            
        elif badanie.status==Status.reconstructing:
            cluster.status_rekonstrukcji()
            
        elif badanie.status==Status.finished_reconstruction:
            #anonimizacja danych
            cluster.anonimizacja()
            
        elif badanie.status==Status.trwa_anonimizacja:
            cluster.status_anonimizacji()
            
        elif badanie.status==Status.finished_anonimization:
            cluster.budowanie_koncowego_obrazu()
            
        elif badanie.status==Status.finished_analysis:
            cluster.wyslanie_danych()
            
        elif badanie.status==Status.budowanie_koncowego_obrazu:
            controller.zapisz_koncowe_dane()
            #nie mam pliku c-store
        elif badanie.status==Status.procedura_zakonczona:
            cykl=False
    return
run()    