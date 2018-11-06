import pydicom
import argparse


class UI():
    """
    Klasa implementująca interfejs użytkownika.
    """
    
    
    def query(argv=None):
        """
        Metoda, dzięki której personel medyczny przez wpisanie imienia i nazwiska może znalezc z posrod wielu pacjentów tego konkretnego 
    
        """
        parser = argparse.ArgumentParser(description='There is User Interface. You can find patient or examination. Type in patient name and surname')
        Patient_name= parser.add_argument('-n','--name', help='Please, type in patient name', required=False)
        Patient_surname= parser.add_argument('-s','--surname', help='Please, type in patient surname',required=True)
        args = parser.parse_args()    
        print("Finding examination for:  %s %s" % (args.name, args.surname))   
        with pydicom.dcmread("worklist_query.dcm", force=True) as ds:
            ds.PatientName=args.name +" "+ args.surname
            print(ds)
            return Patient_name,Patient_surname
          
    def do_study(list_of_studies):
        """
        Metoda implementująca komunikację z personelem szpitala, a dokładniej personel medyczny może dokonać wyboru, które badanie z listy ma być wykonane

        :param list_of_studies: Lista badań
        
        """
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
    """
    Metoda odpowiedzialna za wyswietlanie komunikatów dotyczących badania
    
    """        
        print(text)