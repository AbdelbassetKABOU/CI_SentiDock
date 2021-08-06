import os
import requests
import database as db
import config as cfg 

api_address = cfg.api_address
api_port = cfg.api_port
myoutput = cfg.authentication_output
database = db.users
volume = cfg.volume
myfile = cfg.logfile


def authentication_test (login, password):
#def authen_test (login, password):
    r = requests.get(
            url='http://{address}:{port}/permissions'.\
            format( address=api_address, port=api_port),
            params= {
                'username': login,
                'password': password
            }
        )

    # statut de la requête
    status_code = r.status_code

    output = myoutput

    # affichage des résultats
    if status_code == 200:
        test_status = 'SUCCESS'
    else:
        test_status = 'FAILURE'

    return  output.format(
               status_code=status_code, 
               test_status=test_status, 
               login=login, 
               password=password
            )
    

# impression dans un fichierA
def file_output(output):
        file_path = volume+myfile  
        with open(file_path, 'a') as file:
            file.write(output)
            file.close()

for key, value in database.items() :
    #output = authen_test (key, value)
    output = authentication_test (key, value['password'])
    if os.environ.get('PRINT') == '1':
        print (output)
    if os.environ.get('LOG') == '1':
        file_output(output)



