
from redis import Redis

r = Redis(host='redis', port=6379)
api_address = r.get('api_address').decode('utf-8')
api_port = int(r.get('api_port').decode('utf-8'))
logfile = r.get('logfile').decode('utf-8')
volume = r.get('volume').decode('utf-8')
content_output = r.get('content_output').decode('utf-8')

"""
# This is how our print-template looks like
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

