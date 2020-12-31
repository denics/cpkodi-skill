from mycroft.util.log import LOG
import requests
import json

def show_movie_info(kodi_path):
    """
        Confirm that Koid i splaying before Executing this script
    """
    api_path = kodi_path + "/jsonrpc"
    json_header = {'content-type': 'application/json'}
    method = "Input.Info"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": 1
    }
    try:
        kodi_response = requests.post(api_path, data=json.dumps(kodi_payload), headers=json_header)
        return kodi_response
    except Exception as e:
        LOG.error(e)
