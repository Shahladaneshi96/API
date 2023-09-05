import asyncio
from rasa.core.agent import Agent
from rasa.shared.utils.io import json_to_string
from parsivar import Normalizer
from parsivar import SpellCheck

class Classifier:
    def __init__(self, slot_filling_model_path: str, semantic_model_path: str):
        self.slot_filling_agent = Agent.load(slot_filling_model_path)
        self.semantic_agent = Agent.load(semantic_model_path)

    @staticmethod
    def normalizer(text):
        clean_text = text
        # normalizer = Normalizer()
        # normalized_text = normalizer.normalize(text)
        # spell_checker = SpellCheck()
        # clean_text = spell_checker.spell_corrector(normalized_text)
        return clean_text

    def send_request_to_Rasa(self, agent, message: str) -> str:
        message = message.strip()
        result = asyncio.run(agent.parse_message(message))
        return json_to_string(result)

    def inference_slot_filling(self, user_message, user_id):
        normalized_message = self.normalizer(user_message)
        response = self.send_request_to_Rasa(self.slot_filling_agent, normalized_message)
        return response

    def inference_semantic(self, user_message, user_id):
        normalized_message = self.normalizer(user_message)
        response = self.send_request_to_Rasa(self.semantic_agent, normalized_message)
        return response

# Usage
slot_filling_model_path = '/home/shahla_daneshi/classifier-zahra/models/nlu-20230830-221145-proud-assignment.tar.gz'
semantic_model_path = '/home/shahla_daneshi/classifier-zahra/models1/nlu-20230829-223810-presto-consultant.tar.gz'
user_message = "سلام"
user_id = "shahla"

model_loader = Classifier(slot_filling_model_path, semantic_model_path)
data_from_slot_filling = model_loader.inference_slot_filling(user_message, user_id)
data_from_semantic = model_loader.inference_semantic(user_message, user_id)
print('----------------******data_from_slot_filling****----------:', data_from_slot_filling)

print('----------------*********data_from_semantic*******---------:', data_from_semantic)
