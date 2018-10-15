#Collection of libraries
import pydicom
from bazadanych2aa import Catalog, Study, Status
import time
import argparse
import os
import shutil
import time
import datetime

#Controller class
class controller():
    def find_study():    
        list_of_files=[]
        dicom_file= pydicom.dcmread("worklist_rsp.dcm", force=True)
        list_of_files.append(dicom_file)
        print(list_of_files)
        return list_of_files
        
        
    def get_study_list(identifier):
        ncreate=pydicom.dcmread("mpps2.dcm", force=True)
        examination= Catalog.get(identifier)
        examination.path="C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\"
        Catalog.commit()
        return
          
    
    def status():
        time.sleep(1)
        return print("The protocol has been prepared")
        
        
    def save_final_data(identifier):
        time.sleep(1)
        examination= Catalog.get(identifier)
        examination.status=Status.procedure_completed
        Catalog.commit()
        print("Final data are saved")
        return               

   #Building final image and deanonymisation     
    def build_final_image(identifier):
        examination = Catalog.get(identifier)
        examination.status=Status.build_final_image
        Catalog.commit()
#zmien sciezke
        pie='C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\cluster\\id1.jpg'
        dru='C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\cluster\\koncowy.jpg'
        
        os.rename(pie,dru) 
        
        time.sleep(1)
        print("Trwa budowanie koncowego obrazu")
        return



#Scanner class 
class scanner():
    #Communication with scanner PET 
    def scan(identifier):
        examination = Catalog.get(identifier)
        examination.status=Status.scanning
        Catalog.commit()
        return print("Scanning patient")  
        
    # Current scan status verification  
    def scan_status(identifier):
        examination = Catalog.get(identifier)
        examination.status=Status.finished_scanning
        Catalog.commit()
        time.sleep(1)
        return print("The Scan was executed") 

    # Sending scan results from scanner PET to controller                 
    def send_scan_results(identifier):
        time.sleep(1)
        examination = Catalog.get(identifier)
        examination.status=Status.send_raw_data
        Catalog.commit()
        scanner_pet = "C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\scanner\\id1.jpg"
        examination.raw_data_file = "C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\controller"
        shutil.copy(scanner_pet,examination.raw_data_file)
        
        
        #usun?
        #result = open('scan.txt', 'w')                                           #(1)
        #data=result.read()
        #result.close()
        return print("The results were sent to the controller")#,data
         
#User interface Class
class UI():
    def query(argv=None):
        parser = argparse.ArgumentParser(description='There is User Interface. You can find patient or examination. Type in patient name and surname')
        Patient_name= parser.add_argument('-n','--name', help='Please, type in patient name', required=False)
        Patient_surname= parser.add_argument('-s','--surname', help='Please, type in patient surname',required=True)
        args = parser.parse_args()    
        text=print("Finding examination for:  %s %s" % (args.name, args.surname))   
        #Entering parameters from UI to the empty worklist
        with pydicom.dcmread("worklist_query.dcm", force=True) as ds:
            ds.PatientName=args.name +" "+ args.surname
            return Patient_name,Patient_surname, text, print(ds)
          
    
    def do_study(list_of_studies):
        while True:
            try:
                confirmation=int(input("Specify number of examination which you want to commision: "))
                if confirmation<=int(len(list_of_studies)-1):
                    wys=print("Zakończono sporządzanie danych do badania")
                    break
                else:
                    print("Incorrect number of examination, try again")
            except (ValueError, UnboundLocalError):
                print("You don't type integer, try again")
            except IndexError:
                print("Incorrect number of examination, try again")
        return confirmation
    
    
    def communique(identifier):
        return print("The test failed")

# Cluster class
class cluster():
    #Sending input data from controller to cluster
    def send_input_data(identifier):
        time.sleep(1)
        source3 = "C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\controller\\id1.jpg"
        destination3 = "C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\cluster"
        shutil.copy(source3,destination3)
        # czytanei pliku z bazy danych
        examination = Catalog.get(identifier)
        examination.status=Status.reco_data_ready
        Catalog.commit()
        return print("Downloading input data for reconstruction")

    #Reconstruction registered    
    def register(identifier):
        time.sleep(1)
        examination = Catalog.get(identifier)
        examination.status=Status.reco_registered
        Catalog.commit()
        return print("Reconstruction registered")

    #Reconstruction queued
    def start_reconstruction(identifier):
        time.sleep(1)
        examination = Catalog.get(identifier)
        examination.status=Status.reco_queued
        Catalog.commit()
        return print("Reconstruction queued")
    
    #
    def status(identifier):
        time.sleep(1)
        examination = Catalog.get(identifier)
#        if examination.status==Status.reco_queued:
#            examination.status=Status.reco_running
#        elif examination.status==Status.reco_running:
        examination.status=Status.reco_finished        
        Catalog.commit()
        return 

    # Data anonymisation    
    def anonymisation(identifier):
        time.sleep(1)
        examination = Catalog.get(identifier)
        examination.status=Status.finished_anonymisation
        Catalog.commit()
        return
    
    # Get final output data from cluster to controller
    def get_output_data(identifier):
        examination = Catalog.get(identifier)
        examination.status=Status.send_final_data
        Catalog.commit()
        cluster = "C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\cluster\\koncowy.jpg"
        examination.final_image = "C:\\Users\\Anna\\Desktop\\pynetdicom_git_clone\\pynetdicom3\\pynetdicom3\\apps\\findscu\\controller"
        shutil.copy(cluster,examination.final_image)
        time.sleep(1)
        return print("The results have been sent")


# Core mechanism     
def run():
    UI.query()
    list_of_examinations=controller.find_study()
    number=UI.do_study(list_of_examinations)
    # Creating the examination object:
    examination_id= Catalog.newstudy(patient_name=str(list_of_examinations[number].PatientName),
                              patient_id=list_of_examinations[number].PatientID,
                              start_date=datetime.datetime.strptime(list_of_examinations[number].ScheduledProcedureStepSequence[0].ScheduledProcedureStepStartDate,'%Y%m%d'),
                              end_date=datetime.datetime.strptime(list_of_examinations[number].ScheduledProcedureStepSequence[0].ScheduledProcedureStepEndDate,'%Y%m%d'),
                              aetitle=list_of_examinations[number].ScheduledProcedureStepSequence[0].ScheduledStationAETitle,
                              status="new",
                              final_image=None,
                              raw_data_file=None,
                              path_mpps=None)
    controller.get_study_list(examination_id)
    controller.status()    
    loop=True   
    while(loop):
        examination=Catalog.get(examination_id)
        if examination.status==Status.new:
            scanner.scan(examination_id)
            print(examination.status)
        elif examination.status==Status.scanning:        
            scanner.scan_status(examination_id)
        elif examination.status==Status.finished_scanning:
            #Sending raw data from the scanner to the controller
            scanner.send_scan_results(examination_id)            
        elif examination.status==Status.send_raw_data:
            cluster.anonymisation(examination_id)            
        elif examination.status==Status.finished_anonymisation:   
            cluster.register(examination_id)
        elif examination.status==Status.reco_registered:
            cluster.send_input_data(examination_id)
        elif examination.status==Status.reco_data_ready:
            cluster.start_reconstruction(examination_id)
        elif examination.status==Status.reco_queued or examination.status == Status.reco_running:    
            cluster.status(examination_id)
        elif examination.status==Status.reco_finished:
            controller.build_final_image(examination_id)                
        elif examination.status==Status.build_final_image:
            cluster.get_output_data(examination_id)           
        elif examination.status==Status.send_final_data:
            controller.save_final_data(examination_id)
        elif examination.status==Status.procedure_completed:
            loop=False
        elif examination.status==Status.failed:
            UI.communique(examination_id)
            loop=False
    return
run()    