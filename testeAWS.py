import requests

base_url = 'http://a0b7509a39ef44d2c88e564449cbc285-890461114.us-east-2.elb.amazonaws.com'

register_data = {
    "nome": "Disciplina Cloud",
    "email": "thiagosousa1@insper.edu.br",
    "senha": "1234"
}
response = requests.post(f'{base_url}/registrar', json=register_data)
print(f'Registro - Status Code: {response.status_code}')
print(f'Registro - Resposta: {response.json()}')

login_data = {
    "email": "thiagosousa1@insper.edu.br",
    "senha": "1234"
}
response = requests.post(f'{base_url}/login', json=login_data)
print(f'Login - Status Code: {response.status_code}')
print(f'Login - Resposta: {response.json()}')

token = response.json().get('jwt')

print(f'token: {token}')

if token:
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(f'{base_url}/consultar', headers=headers)
    print(f'Consultar - Status Code: {response.status_code}')
    print(f'Consultar - Resposta: {response.json()}')
else:
    print("Token não recebido.")
