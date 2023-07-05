from decouple import config
import json
from requests import get, Session
from time import sleep
from urllib.parse import urljoin
import logging

# Load configuration values from .env file or environment variables
# Server configuration - URL and Access token configuration of the Supla Cloud service (https://cloud.supla.org/)
SERVER = config('SERVER')
PERSONAL_ACCESS_TOKEN = config('PERSONAL_ACCESS_TOKEN')
# Fronius service-related configuration
ID = config('ID')
# PV_URL for Fronius service - URL for accessing the Fronius API
PV_URL = config('PV_URL') + "solar_api/v1/GetPowerFlowRealtimeData.fcgi"

# Set up base URL and session for API requests
base_url = f'https://{SERVER}/api/'
session = Session()
session.headers['Authorization'] = f'Bearer {PERSONAL_ACCESS_TOKEN}'
log_file = 'app.log'
counter = 0

# Configure logging
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
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
    counter += 1
    logger.info("*"*20)
    pv_value = fetch_pv_value(PV_URL)  # Log separator
    logger.info(f'Current power PV: {pv_value}')  # Log current PV power value

    # Check if PV value exceeds threshold and device state needs to be updated
    if pv_value > 2999 and not fetch_device_state(ID):
        update_device_parameters(ID, {"action": "TURN_ON"})
        logger.info("Device is turn ON" if fetch_device_state(ID) else "Device is turn OFF")
    elif pv_value < 2999 and fetch_device_state(ID):
        update_device_parameters(ID, {"action": "TURN_OFF"})
        logger.info("Device is turn ON" if fetch_device_state(ID) else "Device is turn OFF")
    else:
        logger.info("No state change")  # Log when no state change occurs
    sleep(600)  # Sleep for 10 minutes
    if counter == 144:
        counter = 0
        with open(log_file, 'w') as file:
            file.write('')  # Clear log file at the end of the day
