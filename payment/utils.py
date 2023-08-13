from django.contrib.gis.geoip2 import GeoIP2

from ipware import get_client_ip
import requests
from decimal import Decimal
import environ

env = environ.Env()
environ.Env.read_env()

def check_if_user_has_subscription(user):
    return user.subscription_set.filter(
        is_active=True,
    ).exists()
    
def get_currency_code(country_code):
    response = requests.get(f"https://restcountries.com/v2/alpha/{country_code}")
    data = response.json()
    if 'currencies' in data:
        currency = data['currencies'][0]
        return currency['code']
    else:
        return None
    
def get_exchange_rate(base_currency, target_currency):
    OPEN_EXCHANGE_RATES_APP_ID = env('OPEN_EXCHANGE_RATES_APP_ID')
    url = f'https://openexchangerates.org/api/latest.json?app_id={OPEN_EXCHANGE_RATES_APP_ID}&base={base_currency}&symbols={target_currency}'
    response = requests.get(url)
    data = response.json()
    return data['rates'][target_currency]

def get_currency_from_ip(ip_address):
    g = GeoIP2()
    country_code = g.country(ip_address)['country_code']
    currency_code = get_currency_code(country_code)
    return currency_code

def convert_currency(amount, from_currency_code, to_currency_code):
    exchange_rate = get_exchange_rate(from_currency_code, to_currency_code)
    return amount * exchange_rate

def convert_price(request, from_currency, amount):
    # ip, is_routable = get_client_ip(request)
    ip = '184.147.189.60'
    currency_code = get_currency_from_ip(ip)
    target_price = convert_currency(amount, from_currency, currency_code)
    target_price = Decimal(target_price).quantize(Decimal('.01'))
    return target_price, currency_code
