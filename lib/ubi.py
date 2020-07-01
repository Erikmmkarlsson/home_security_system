import urequests as requests
import keys

TOKEN = keys.ubidots_token #Import your key from key file

# Builds the json to send the request
def build_json(variable1, value1, variable2, value2, variable3, value3):
    try:
        data = {variable1: {"value": value1},
                variable2: {"value": value2},
                variable3: {"value": value3}}
        return data
    except:
        return None


# Sends the request. Please reference the REST API reference https://ubidots.com/docs/api/
def post_var(device, value1, value2, value3):
    try:
        url = "https://industrial.api.ubidots.com/"
        url = url + "api/v1.6/devices/" + device
        headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
        
        # Here you can edit the labels
        data = build_json(
        "Temperature", value1, 
        "Smoke", value2, 
        "Movement", value3
        )
        if data is not None:
            print(data)
            req = requests.post(url=url, headers=headers, json=data)
            return req.json()
        else:
            pass
    except:
        pass
