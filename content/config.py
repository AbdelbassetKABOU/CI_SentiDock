
from redis import Redis

r = Redis(host='redis', port=6379)
api_address = r.get('api_address').decode('utf-8')
#api_address = '172.17.0.3'  
# port de l'API
api_port = int(r.get('api_port').decode('utf-8'))
logfile= r.get('logfile').decode('utf-8')
volume=r.get('volume').decode('utf-8')
# définition de l'adresse de l'API
#api_address = '172.17.0.2'



"""
# définition de l'adresse de l'API
api_address = 'sentiment'
# port de l'API
api_port = 8000
logfile='api_test.log'
volume='/home/cicd_vol/'
"""
content_output = r.get('content_output').decode('utf-8')
"""
print ('-------------------------')
print ('-------------------------')
print ("  ", content_output)
print ('-------------------------')
print ('-------------------------')
"""
"""
content_output = 
             ============================
                     Content test
             ============================
             
             request done at "/v1/sentiment"
                           & "/v2/sentiment"
                 | username={login}
                 | sentence={sentence} 
             
             expected result = {expected_code}
             actual restult = {status_code}
             
             ==>  {test_status}
"""

