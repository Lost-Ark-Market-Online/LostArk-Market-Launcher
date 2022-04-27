import requests
from modules.config import update_token
from modules.errors import LoginError, NoTokenError

api_key = 'AIzaSyBMTA0A2fy-dh4jWidbAtYseC7ZZssnsmk'


def login(email, password):
    res = requests.post(f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}', json={
        'email': email,
        'password': password,
        'returnSecureToken': True
    })
    tokens = res.json()
    if 'error' in tokens:
        raise LoginError()
    update_token({
        "id_token": tokens['idToken'],
        "refresh_token": tokens['refreshToken'],
        "uid": tokens['localId'],
    })
    return tokens['idToken'], tokens['refreshToken'], tokens['localId']


def refresh_token(token):
    res = requests.post(f'https://securetoken.googleapis.com/v1/token?key={api_key}', json={
        'refresh_token': token,
        'grant_type': 'refresh_token'
    })
    tokens = res.json()
    if 'error' in tokens:
        raise NoTokenError()
    update_token({
        "id_token": tokens['id_token'],
        "refresh_token": tokens['refresh_token'],
        "uid": tokens['user_id'],
    })
    return tokens['id_token'], tokens['refresh_token'], tokens['user_id']
