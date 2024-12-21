import requests

token_url     = "http://localhost:8000/techtest/token"
validator_url = "http://localhost:8000/techtest/token"
code_url      = "http://localhost:8000/techtest/source"

token = requests.get(token_url).text
validation_response = requests.post(validator_url, headers={'Content-Type': 'text/plain'}, data=token)
print(validation_response.text)
assert validation_response.status_code == 200, "VALIDATION FAILED"
print("[SECRET] ", validation_response.json()["secret"])

source_code_response = requests.get(code_url, params={"secret": validation_response.json()["secret"]})
print("[SOURCE CODE REPONSE] ", source_code_response.text)
assert source_code_response.status_code == 200, "Cannot retrieve source code"
print(source_code_response.text)
