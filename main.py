from datetime import datetime
from decouple import config
import json
from requests import get, Session
from time import sleep
from urllib.parse import urljoin
import logging

# Load configuration values from .env file or environment variables
SERVER = config('SERVER')
PERSONAL_ACCESS_TOKEN = config('PERSONAL_ACCESS_TOKEN')
ID = config('ID')
PV_URL = config('PV_URL')

# Set up base URL and session for API requests
base_url = f'https://{SERVER}/api/'
session = Session()
session.headers['Authorization'] = f'Bearer {PERSONAL_ACCESS_TOKEN}'

# Konfiguracja logowania
logging.basicConfig(filename='/var/www/html/app.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

def fetch_device_state(id_device):
    # Fetch the state of the device with the given id_device
    with session.get(urljoin(base_url, f'channels/{id_device}')) as resp:
        data = resp.json()
    return data['on']


def update_device_parameters(id_device, parameter):
    # Update the device parameters with the provided parameter object
    with session.patch(
        urljoin(base_url, f'channels/{id_device}'),
        json=parameter
    ) as resp:
        return resp


def fetch_pv_value(url):
    # Fetch the PV value from the provided URL
    return int(json.loads(get(url).text)['Body']['Data']['Site']['P_PV'])


while True:
    logger.info("*"*20)
    logger.info(datetime.now().strftime("%H:%M:%S"))
    pv_value = 4000 #fetch_pv_value(PV_URL)
    logger.info(f'Current power PV: {pv_value}')

    # Check if PV value exceeds threshold and device state needs to be updated
    if pv_value > 2999 and not fetch_device_state(ID):
        update_device_parameters(ID, {"action": "TURN_ON"})
        logger.info("Device is turn ON" if fetch_device_state(ID) else "Device is turn OFF")
    elif pv_value < 2999 and fetch_device_state(ID):
        update_device_parameters(ID, {"action": "TURN_OFF"})
        logger.info("Device is turn ON" if fetch_device_state(ID) else "Device is turn OFF")
    else:
        logger.info("Didn't change stata")
    sleep(3)