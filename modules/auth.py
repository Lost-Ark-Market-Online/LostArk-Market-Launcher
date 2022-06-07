import requests
from modules.config import Config
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
    Config().update_token({
        "id_token": tokens['idToken'],
        "refresh_token": tokens['refreshToken'],
        "uid": tokens['localId'],
    })


def refresh_token(token):
    res = requests.post(f'https://securetoken.googleapis.com/v1/token?key={api_key}', json={
        'refresh_token': token,
        'grant_type': 'refresh_token'
    })
    tokens = res.json()
    if 'error' in tokens:
        raise NoTokenError()
    Config().update_token({
        "id_token": tokens['idToken'],
        "refresh_token": tokens['refreshToken'],
        "uid": tokens['localId'],
    })
