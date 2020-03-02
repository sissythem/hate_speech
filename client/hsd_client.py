from os import getcwd
from os.path import join, exists
import requests
import json
import yaml


def read_credentials():
    credentials_file = join(getcwd(), "credentials.yaml")
    if not exists(credentials_file):
        return False
    else:
        with open(credentials_file, "r") as f:
            return yaml.safe_load(f)


def login():
    credentials = read_credentials()
    data = {
        "username": credentials["username"],
        "password": credentials["password"]
    }

    r = requests.post(credentials["host"] + '/users/login/', data=json.dumps(data))
    if r.status_code == 200:
        response = json.loads(r.text)
        # return {"access_token": response["access_token"], "refresh_token": response["refresh_token"]}
        return response
    else:
        print("Could not authenticate user!")


def exec_nlp_semantic_augmentation(file_path):
    credentials = read_credentials()
    params = (
        ('', ''),
        ('', ),
        ('', ),
    )
    files = {
        'file': (file_path, open(file_path, 'rb')),
    }
    _r = requests.post(credentials["host"] + '/sem-augm/exec_nlp/', params=params, files=files)
    return _r.text
