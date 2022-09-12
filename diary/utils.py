import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def get_client_ip(request):
    ip = None
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


def get_weather_info(request):
    client_ip = get_client_ip(request)
    if not client_ip or client_ip == '127.0.0.1':
        client_ip = 'Seoul'

    url = 'http://api.weatherapi.com/v1'
    api_method = '/current.json'
    params = {
        'key': settings.WEATHER_API_KEY,
        'q': client_ip,
        'lang': 'ko',
    }
    response = requests.get(f'{url}{api_method}', params=params).json()

    if 'error' in response:
        error_code = response['error']['code']
        error_message = response['error']['message']
        logger.error(f"ERROR: weather API [ERR {error_code}] {error_message}")
        return None

    current_weather = response['current']['condition']['text']
    return current_weather
