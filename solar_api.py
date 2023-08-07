from fastapi import FastAPI

app = FastAPI()


@app.get("/solar_api/v1/GetPowerFlowRealtimeData.fcgi")
def get_success():
    data = {
        "Body": {
            "Data": {
                "Inverters": {
                    "1": {
                        "Battery_Mode": "normal",
                        "DT": 99,
                        "E_Day": 6758,
                        "E_Total": 7604385.5,
                        "E_Year": 1342638.25,
                        "P": 506,
                        "SOC": 55,
                    }
                },
                "Site": {
                    "BatteryStandby": False,
                    "E_Day": 6758,
                    "E_Total": 7604385.5,
                    "E_Year": 1342638.2000000002,
                    "Meter_Location": "grid",
                    "Mode": "bidirectional",
                    "P_Akku": -384.70000000000005,
                    "P_Grid": -511.99000000000001,
                    "P_Load": 5.9900000000000091,
                    "P_PV": 941.60000000000002,
                    "rel_Autonomy": 100,
                    "rel_SelfConsumption": 0,
                },
                "Smartloads": {
                    "Ohmpilots": {
                        "720897": {
                            "P_AC_Total": 2635,
                            "State": "normal",
                            "Temperature": 30.7,
                        }
                    }
                },
                "Version": "12",
            }
        },
        "Head": {
            "RequestArguments": {},
            "Status": {"Code": 0, "Reason": "", "UserMessage": ""},
            "Timestamp": "2019-06-12T15:31:07+02:00",
        },
    }

    return data
