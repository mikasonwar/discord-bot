import requests

class Jokes():
    def __init__(self):
        self.api_url = "https://v2.jokeapi.dev/joke/Any"

    def get_joke(self):
        try:
            r = requests.get(self.api_url)
            r.raise_for_status()
            obj = r.json()
        except Exception as e:
            return "deu erro a fazer o request"

        if r.status_code != 200:
            return "deu erro loles"

        if obj["type"] == "twopart":
            return f'{obj["setup"]} \n\n||{obj["delivery"]}||'
        else:
            return obj["joke"]