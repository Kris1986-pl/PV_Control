from main import fetch_device_state, env_is_dev, fetch_pv_value
from decouple import config

ID = config('ID')


def test_fetch_pv_value_is_positive_number():
    pv_value = fetch_pv_value()
    assert pv_value > 0


def test_fetch_device_state_valid_id():
    id_device = ID
    expected_state_type = bool
    assert type(fetch_device_state(id_device)) == expected_state_type


def test_fetch_device_state_invalid_id():
    id_device = 1
    expected_state = -1
    assert fetch_device_state(id_device) == expected_state


def test_env_is_dev():
    assert env_is_dev() is True
