import requests
import json

# json_data = {"value1": 3}
# headers = {'Content-Type': 'application/json'}

# requests.post(
#     'https://maker.ifttt.com/trigger/start_alarm/with/key/ehsWG5yTpSDi6wmh7X20wWEiEWk4FoMLocB2hc1eLOh', data=json.dumps(json_data), headers=headers)

requests.post(
    'https://maker.ifttt.com/trigger/stop_alarm/with/key/ehsWG5yTpSDi6wmh7X20wWEiEWk4FoMLocB2hc1eLOh')
