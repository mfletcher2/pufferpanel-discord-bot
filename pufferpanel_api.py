import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
client_id = os.getenv('PUFFERPANEL_CLIENTID')
client_secret = os.getenv('PUFFERPANEL_SECRET')

url = os.getenv('PANEL_URL')


def get_header():
    request_data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    }

    r = requests.post(url + '/oauth2/token', data=request_data)
    token = r.json()['access_token']
    return {'Authorization': 'Bearer ' + token}


def get_user_info() -> json:
    r = requests.get(url + '/api/users', headers=get_header())
    return r.json()


def get_servers() -> dict:
    print('Getting servers')
    r = requests.get(url + '/api/servers', headers=get_header())
    name_to_id = dict()
    for server in r.json()['servers']:
        name_to_id[server['name']] = server['id']
    return name_to_id


def start_server(server_id: str):
    print('Starting server ' + server_id)
    r = requests.post(url + '/proxy/daemon/server/' + server_id + '/start', params={}, headers=get_header())


def stop_server(server_id: str):
    print('Stopping server ' + server_id)
    r = requests.post(url + '/proxy/daemon/server/' + server_id + '/stop', params={}, headers=get_header())


def get_server_status(server_id: str) -> bool:
    print('Getting server status for ' + server_id)
    r = requests.get(url + '/proxy/daemon/server/' + server_id + '/status', headers=get_header())
    return r.json()['running']
