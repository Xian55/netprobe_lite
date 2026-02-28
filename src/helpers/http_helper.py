import requests
import json

class CallHome(object): # Call home http functions

    def __init__(self):
        pass

    def post_stats(self,url,stats):

        headers={"Content-Type":"application/json"}

        try:
            request = requests.post(url, data=stats, headers=headers, timeout=10)
            return (request.status_code, request.content)
        except requests.exceptions.RequestException as e:
            print(f"HTTP request failed: {e}")
            return (0, str(e))
