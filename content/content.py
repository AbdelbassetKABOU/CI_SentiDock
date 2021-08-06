import os
import requests
import database as db
import config as cfg 
import json

api_address = cfg.api_address
api_port = cfg.api_port
myoutput = cfg.content_output


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
    # statut de la requête
    # How do I read a response from Python Requests?
    # https://stackoverflow.com/questions/18810777/how-do-i-read-a-response-from-python-requests
    # How to convert bytes type to dictionary?
    # https://stackoverflow.com/questions/49184578/how-to-convert-bytes-type-to-dictionary
    r_v1 = json.loads(r_v1.content.decode('utf-8')) 
    r_v2 = json.loads(r_v2.content.decode('utf-8')) 
    polarity = lambda x: 1 if x>0 else -1
    status_code = (polarity(r_v1['score']), polarity(r_v2['score']))
    expected_code = (v1, v2)
    output = myoutput
    '''
    return """ for {}, 
               expected output : {} 
               actual status_code = {}""".format(sentence, expected_code, status_code)
    '''

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
#login, password = 'alice', db['alice']['password']
login, password = 'alice', 'wonderland'
database = db.sentences
volume = cfg.volume
myfile = cfg.logfile

#"""
# impression dans un fichierA
def file_output(output):
    #if os.environ.get('LOG') == 1:
        file_path = volume+myfile
        with open(file_path, 'a') as file:
            file.write(output)
            file.close()
#"""


for key, value in database.items() :
    output = content_test (login, password, key, value['v1'], value['v2'])
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
