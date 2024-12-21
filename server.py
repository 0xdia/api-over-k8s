import fastapi
import datetime
import random
import inspect
import os

app = fastapi.FastAPI()

secret_seed = os.getenv( 'SECRET', default='my-default-secret' )
random.seed( secret_seed )
SECRET = "".join( random.choices("azertyuiopqsdfghjklmwxcvbn,;:!§/\\*$?", k=100) )

SOURCE_CODE = inspect.getsource(inspect.getmodule(inspect.currentframe()))

def _hash(size=10, seed=None):
    if not seed:
        random.seed( int( datetime.datetime.now().timestamp()) )
    else:
        random.seed( seed )
    return "".join( random.choices("azertyuiopqsdfghjklmwxcvbn,;:!§/\\*$?", k=size) )


@app.get('/', response_class=fastapi.responses.PlainTextResponse)
def instructions(r: fastapi.requests.Request):
    '''
    endpoint to get instructions
    '''

    return f'''
Instructions
---

# Task 1
  The test application you're currently using contains some other endpoints
  -> GET {r.base_url}docs 
     the documentation

  -> GET {r.base_url}token
     to retrieve a token
  
  -> POST {r.base_url}token
     to validate the token + retrieve a _secret_
    
  -> GET {r.base_url}source
     to obtain the source code of the test application (you need the _secret_ from /techtest/token)

  You need to write a script (bash / sh / python / perl / ...) to retrieve the application source code and store it in 'verificator.py'.

# Task 2
  -> at the end of exo 1 you get the source code of the test application
  You need to write a Dockerfile to containerize this application

# Task 3
  You need to write one (or more) Kubernetes manifest(s) to run this application in a Kubernetes cluster

# Task 4
  Whatever you may find interesting to say about this test (issues / optimizations / ...)

# Task 5
  A small reverse proxy configuration ?

--- Output
  - The source code retrieval script
  - The Dockerfile
  - Kubernetes Manifest(s)
  - Brief documentation on how to use your scripts/files
  - A proxy configuration
'''

@app.get('/techtest/token', response_class=fastapi.responses.PlainTextResponse)
def show_token():
    '''
    display ascii art with a embed token
    '''
    date_value = datetime.datetime.now().isoformat()
    token_value = _hash(len(date_value))
    return token_value

@app.post('/techtest/token')
def verify_token( token_value:str  = fastapi.Body(..., embed=False)):
    '''
    accept a token in the request body.
    it accept token up to 3 sec late

    it give you a secret
    '''
    seed = int( datetime.datetime.now().timestamp())
    for i in range(4):
        hash_true_value = _hash(size=len(token_value), seed=seed-i)
        if token_value == hash_true_value: return {"status": "ok", "token": token_value, "lateness": i, "secret": SECRET}
    return {"status": "ko"}

@app.get('/techtest/source', response_class=fastapi.responses.PlainTextResponse)
def obtain_source_code(secret):
    '''
    you need a secret parameter to obtain the source code
    
    the secret is given by the POST /techtest/token endpoint
    '''
    if secret != SECRET:
        return "Find the secret by verifying the token"
    else:
        return SOURCE_CODE

