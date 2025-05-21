import requests
from flask import request

def get_country_from_ip(ip):
    try:
        response = requests.get(f'https://ipapi.co/{ip}/country/')
        if response.status_code == 200:
            return response.text.strip()
    except Exception as e:
        print(f"IP lookup error: {e}")
    return 'US'  # Default fallback

def get_user_lang():
    lang = request.cookies.get('lang')
    if lang in ['en', 'es']:
        return lang

    ip = request.remote_addr or '8.8.8.8'  # fallback IP if none
    country = get_country_from_ip(ip)
    return 'es' if country == 'EC' else 'en'
