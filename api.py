import requests
import json
from parsivar import Normalizer
from parsivar import SpellCheck

class Classifier:
    def __init__(self, api_url_slot_filling, api_url_semantic):
        self.api_url_slot_filling = api_url_slot_filling
        self.api_url_semantic = api_url_semantic

    @staticmethod
    def normalizer(text): 
        # normalizer = Normalizer()
        # normalized_text = normalizer.normalize(text)
        # spell_checker = SpellCheck()
        # clean_text = spell_checker.spell_corrector(normalized_text)
        return text


    def send_request_to_Rasa(self, api_url, message, sender_id):
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        payload = {'message': message, 'sender': sender_id}
        try:
            response = requests.post(api_url, headers=headers, json=payload)
            return response
        except Exception as e:
            print(f"An error occurred while sending a request to Rasa: {str(e)}")
            return None

    def inference_slot_filling(self, user_message, user_id):
        try:
            normalized_message = self.normalizer(user_message)
            response = self.send_request_to_Rasa(self.api_url_slot_filling, normalized_message, user_id)
            if response and response.status_code == 200:
                received_message = json.loads(response.text)
                return received_message
            else:
                print(f"Failed to load data from slot filling API: Status Code {response.status_code if response else 'Unknown'}")
                return None

        except Exception as e:
            print(f"An error occurred while loading data from slot filling API: {str(e)}")
            return None

    def inference_semantic(self, user_message, user_id):
        try:
            normalized_message = self.normalizer(user_message)
            response = self.send_request_to_Rasa(self.api_url_semantic, normalized_message, user_id)
            if response and response.status_code == 200:
                received_message = json.loads(response.text)
                return received_message
            else:
                print(f"Failed to load data from inference semantic API: Status Code {response.status_code if response else 'Unknown'}")
                return None

        except Exception as e:
            print(f"An error occurred while loading data from inference semantic API: {str(e)}")
            return None

# Usage
api_url_slot_filling = 'http://79.143.84.170:5030/webhooks/rest/webhook'
api_url_semantic = 'http://79.143.84.170:5011/webhooks/rest/webhook'
user_message = "سلام"
user_id = "shahla"

api_loader = Classifier(api_url_slot_filling, api_url_semantic)
data_from_slot_filling = api_loader.inference_slot_filling(user_message, user_id)
data_from_semantic = api_loader.inference_semantic(user_message, user_id)
print('data_from_slot_filling:', data_from_slot_filling)
print('data_from_semantic:', data_from_semantic)
