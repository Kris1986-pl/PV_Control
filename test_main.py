from main import fetch_device_state
from decouple import config

ID = config('ID')


def test_fetch_device_state_valid_id():
    id_device = ID
    expected_state_type = bool
    assert type(fetch_device_state(id_device)) == expected_state_type


def test_fetch_device_state_invalid_id():
    id_device = 1
    expected_state = -1
    assert fetch_device_state(id_device) == expected_state
