
from redis import Redis
  
r = Redis(host='redis', port=6379)
#r = Redis(host='172.17.0.2', port=6379)

api_address = r.get('api_address').decode('utf-8')
api_port = int(r.get('api_port').decode('utf-8'))
logfile= r.get('logfile').decode('utf-8')
volume=r.get('volume').decode('utf-8') 
authentication_output = r.get('authentication_output').decode('utf-8') 

"""
authentication_output = '''
             ============================
                 Authentication test
             ============================
             
             request done at "/permissions"
             | username={login}
             | password={password}
             
             expected result = 200
             actual restult = {status_code}
             
             ==>  {test_status}
"""

