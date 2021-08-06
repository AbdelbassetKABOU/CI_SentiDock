import os
import requests
import database as db
import config as cfg 

api_address = cfg.api_address
api_port = cfg.api_port
myoutput = cfg.authorization_output


def authorization_test (login, password, v1, v2):
    r_v1 = requests.get(
            url='http://{address}:{port}/v1/sentiment'.\
            format( address=api_address, port=api_port),
            params= {
                'username': login,
                'password': password,
                'sentence': 'this is a sentence'
            }
        )

    r_v2 = requests.get(
            url='http://{address}:{port}/v2/sentiment'.\
            format( address=api_address, port=api_port),
            params= {
                'username': login,
                'password': password,
                'sentence': 'this is a sentence'
            }
        )
    # statut de la requête
    status_code = (r_v1.status_code, r_v2.status_code)
    expected_code = (v1, v2)
    output = myoutput
    '''return """ for {}, 
               expected output : () 
               actual status_code = {}""".format(login, status_code)'''


    # affichage des résultats
    if status_code == expected_code:
        test_status = 'SUCCESS'
    else:
        test_status = 'FAILURE'

    return  output.format(
               expected_code=expected_code,
               status_code=status_code, 
               test_status=test_status, 
               login=login, 
               password=password
            )

database = db.users
volume = cfg.volume
myfile = cfg.logfile

def file_output(output):
    #if os.environ.get('LOG') == 1:
        file_path = volume+myfile
        with open(file_path, 'a') as file:
            file.write(output)
            file.close()


for key, value in database.items() :
    output = authorization_test (key, value['password'], value['v1'], value['v2'])
    #print (output)
    if os.environ.get('PRINT') == '1':
        print (output)
    if os.environ.get('LOG') == '1':
        file_output(output)




"""
# impression dans un fichier
if os.environ.get('LOG') == 1:
    with open('api_test.log', 'a') as file:
        file.write(output)
"""
