import os
import requests
import database as db
import config as cfg 


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
    status_code = (int(r_v1.status_code==200), int(r_v2.status_code==200))
    expected_code = (int(v1), int(v2))
    output = myoutput

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


def file_output(output):
        file_path = volume+myfile
        with open(file_path, 'a') as file:
            file.write(output)
            file.close()


# my variable 
api_address = cfg.api_address
api_port = cfg.api_port
myoutput = cfg.authorization_output
database = db.users_database
volume = cfg.volume
myfile = cfg.logfile

for key, value in database.items() :
    output = authorization_test (key, value['password'], value['v1'], value['v2'])
    if os.environ.get('PRINT') == '1':
        print (output)
    if os.environ.get('LOG') == '1':
        file_output(output)




