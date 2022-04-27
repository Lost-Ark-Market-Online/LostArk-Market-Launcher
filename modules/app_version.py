import requests


def get_app_version():
    res = requests.get(
        f'https://firestore.googleapis.com/v1/projects/lostarkmarket-79ddf/databases/(default)/documents/app-info/market-watcher')
    return res.json()['fields']['version']['stringValue']
