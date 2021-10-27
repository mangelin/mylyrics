import requests

def helper_retrive_url(url:str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.text

def helper_post_form(url, payload):
    r = requests.post(url, data=payload)
    if r.status_code != 200:
        return None
    return r.text