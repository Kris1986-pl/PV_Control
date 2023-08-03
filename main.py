"""
Module to control a device based on the PV (photovoltaic) power value.
It fetches the real-time PV power value from a Fronius API or a local URL
and updates the state of a device based on a threshold value.

The module requires the following environment variables:
- SERVER: The server URL of the Supla Cloud service.
- PERSONAL_ACCESS_TOKEN: The access token for authentication.
- ID: The ID of the device to control.

The module also requires a .env file to be present in the same directory
with the following configuration:
- PV_URL: The URL for accessing the Fronius API in the development environment.

Note: The PV_URL will be set to a different value in the production environment.

"""
import json
from time import sleep
from os import environ
from urllib.parse import urljoin
import logging
from requests import get, Session, exceptions
from decouple import config


# Load configuration values from .env file or environment variables
# Server configuration - URL and Access token configuration
# of the Supla Cloud service (https://cloud.supla.org/)
SERVER = config('SERVER')
PERSONAL_ACCESS_TOKEN = config('PERSONAL_ACCESS_TOKEN')
# Fronius service-related configuration
ID = config('ID')

if environ.get('ENVIRONMENT') == 'production':
    PV_URL = 'http://localhost/' + "solar_api/v1/GetPowerFlowRealtimeData.fcgi"
    LOG_FILE = 'app.log'
else:
    # PV_URL for Fronius service - URL for accessing the Fronius API
    PV_URL = config('PV_URL') + "solar_api/v1/GetPowerFlowRealtimeData.fcgi"
    LOG_FILE = '/var/www/html/app.log'

# Set up base URL and session for API requests
base_url = f'https://{SERVER}/api/'
session = Session()
session.headers['Authorization'] = f'Bearer {PERSONAL_ACCESS_TOKEN}'

# Configure logging
logging.basicConfig(filename=LOG_FILE,
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)


def fetch_device_state(id_device):
    """
    Fetch the state of the device with the given id_device
    :param id_device: ID form supla's device
    :return: State from supla's device: True or False. If -1 -> Error
    """
    try:
        with session.get(urljoin(base_url, f'channels/{id_device}')) as resp:
            data = resp.json()
        return data['on']
    except KeyError as error:
        logger.error(error)
        return -1


def update_device_parameters(id_device, parameter):
    """
    Update the device parameters with the provided parameter object
    :param id_device: ID form supla's device
    :param parameter: {"action": "TURN_ON"} or {"action": "TURN_OFF"}
    :return: response from API supla.org
    """
    with session.patch(
        urljoin(base_url, f'channels/{id_device}'),
        json=parameter
    ) as response:
        return response


def fetch_pv_value(url):
    """
    :param url: url to API PV System
    :return: The value of moza production from PV. If -1 -> Error
    """
    try:
        response = get(url, timeout=10)
        response.raise_for_status()  # Raises an error if there was an HTTP request error
        data = json.loads(response.text)
        return int(data['Body']['Data']['Site']['P_PV'])
    except (exceptions.RequestException, json.JSONDecodeError, KeyError) as error:
        logger.error("An error occurred while fetching the PV value: %s", str(error))
        return -1
    except ValueError as error:
        logger.error("Unable to convert PV value to int: %s", str(error))
        return -1
    except TypeError as error:
        logger.error(error)
        return -1


while True:
    for counter in range(144):
        logger.info("*"*20)
        pv_value = fetch_pv_value(PV_URL)  # Log separator
        # pv_value = 3000  # Log separator
        logger.info('Current power PV: %s', pv_value)  # Log current PV power value

        # Check if PV value exceeds threshold and device state needs to be updated
        if pv_value > 2999 and not fetch_device_state(ID):
            update_device_parameters(ID, {"action": "TURN_ON"})
            logger.info("Device is turn ON" if fetch_device_state(ID) else "Device is turn OFF")
        elif 0 < pv_value < 2999 and fetch_device_state(ID):
            update_device_parameters(ID, {"action": "TURN_OFF"})
            logger.info("Device is turn ON" if fetch_device_state(ID) else "Device is turn OFF")
        else:
            logger.info("No state change")  # Log when no state change occurs
        sleep(600)  # Sleep for 10 minutes
        if counter == 144:
            with open(LOG_FILE, 'w', encoding='utf-8') as file:
                file.write('')  # Clear log file at the end of the day
