import os
import requests
import database as db
import config as cfg 
import json

api_address = cfg.api_address
api_port = cfg.api_port
myoutput = cfg.content_output
sentences_database = db.sentences_database
users_database = db.users_database
volume = cfg.volume
myfile = cfg.logfile


# First login/password
# Could we get the first login/password from the database
# without knowing the keys :/ 
first_user = list(users_database.values())[0]
login = list(users_database.keys())[0]
password = list(first_user.values())[0] 

def content_test (login, password, sentence, v1, v2):
    r_v1 = requests.get(
            url='http://{address}:{port}/v1/sentiment'.\
            format( address=api_address, port=api_port),
            params= {
                'username': login,
                'password': password,
                'sentence': sentence,
            }
        )

    r_v2 = requests.get(
            url='http://{address}:{port}/v2/sentiment'.\
            format( address=api_address, port=api_port),
            params= {
                'username': login,
                'password': password,
                'sentence': sentence,
            }
        )

    r_v1 = json.loads(r_v1.content.decode('utf-8')) 
    r_v2 = json.loads(r_v2.content.decode('utf-8')) 
    polarity = lambda x: 1 if x>0 else -1
    status_code = (polarity(r_v1['score']), polarity(r_v2['score']))
    expected_code = (int(v1), int(v2))
    output = myoutput

    # affichage des résultats
    if status_code == expected_code:
        test_status = 'SUCCESS'
    else:
        test_status = 'FAILURE'

    return  output.format(
               sentence=sentence,
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

for key, value in sentences_database.items() :
    output = content_test (login, password, key, value['v1'], value['v2'])
    if os.environ.get('PRINT') == '1':
        print (output)
    if os.environ.get('LOG') == '1':
        file_output(output)

