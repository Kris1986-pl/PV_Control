# PV Control

PV Control is a Python script that allows you to integrate and control a Supla device, such as a heater, with your photovoltaic system. It automates the process of enabling or disabling the device based on the power generated by the PV system.

## Quick Start

To quickly get started with PV Control, follow these steps:

1. Clone the repository to your Raspberry Pi device.

2. Install the required dependencies by creating and activating a virtual environment:

   ```shell
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Obtain the necessary configuration values from the Supla Cloud service:

   - `SERVER`: Go to https://cloud.supla.org/ and retrieve the server URL.
   - `PERSONAL_ACCESS_TOKEN`: Generate a personal access token on the Supla Cloud platform.

4. Configure the following parameters in the `.env` file or as environment variables:

   - `SERVER`: The server URL obtained from the Supla Cloud service.
   - `PERSONAL_ACCESS_TOKEN`: The personal access token obtained from the Supla Cloud service.
   - `ID`: The ID of the Supla device.
   - `PV_URL`: The URL for accessing the Fronius PV system data in your local network.
5. Set up a cron job to run the script at system startup. Open the crontab file:

   ```shell
   sudo crontab -e
   ```

6. Add the following line to the crontab file:

   ```shell
   @reboot /home/pi/PV_Control/venv/bin/python /home/pi/PV_Control/main.py > /path/to/output.txt 2>&1
   ```

   Replace `/path/to/output.txt` with the desired path to save the output and error logs.

7. Save the crontab file and exit.

8. Reboot your Raspberry Pi, and the PV Control script will start automatically.

## Case Study

The PV Control script serves as a practical example of integrating a Supla device with a photovoltaic system. It demonstrates how to monitor the power generated by the PV system and control a specific device based on the power thresholds.

## Raspberry Pi

PV Control is designed to run on Raspberry Pi devices. It leverages the GPIO capabilities and the Linux environment provided by Raspberry Pi to interface with the Supla device and monitor the PV system's power.
 note that the `SERVER` and `PERSONAL_ACCESS_TOKEN` values should be obtained from the Supla Cloud service at https://cloud.supla.org/. On the other hand, the `ID` and `PV_URL` parameters should correspond to the specific devices and PV system in your local network.