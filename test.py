import json
import time

import requests

import base64

class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)
    
    def change(self, base64_string):
        image=str.encode(images[0])
        img_data = image

        with open("NW.png", "wb") as fh:
            fh.write(base64.decodebytes(img_data))


if __name__ == '__main__':
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', '1B631D4221B34E1874CBD92A4CEA29D3', 'DB1072C8C40AE7CB3C6FDFE875AB966B')
    model_id = api.get_model()
    uuid = api.generate("Nightwing", model_id)
    images = api.check_generation(uuid)
    print(images)

# def change():
#     image=str.encode(images[0])
#     img_data = image

#     with open("NW.png", "wb") as fh:
#         fh.write(base64.decodebytes(img_data))