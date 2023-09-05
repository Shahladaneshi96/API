import openai

class OutOfScopeHandler:
    def __init__(self, api_key, chat_mode="gpt-3.5-turbo", config=None):
        openai.api_key = api_key
        self.chat_mode = chat_mode
        self.config = config if config else {}

    def handle_out_of_scope(self, user_message):
        prompt = f" Handle the following out-of-scope user message:\"{user_message}\""
        
        request_dict = {
            "model": self.chat_mode,
            "messages": [
                {"role": "system", "content": "You are a Persian-speaking product recommender assistant. Please provide short answers in this domain."},
                {"role": "user", "content": prompt},
            ]
        }

        request_dict.update(self.config)

        response = openai.ChatCompletion.create(**request_dict)

        assistant_reply = response['choices'][0]['message']['content']
        return assistant_reply

if __name__ == "__main__":
    api_key = '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'

    config = {
        "temperature": 0.0,
        "max_tokens": 50
    }

    out_of_scope_handler = OutOfScopeHandler(api_key, config=config)

    out_of_scope_messages = [
        'یه جک تعریف کن'
    ]

    for message in out_of_scope_messages:
        reply = out_of_scope_handler.handle_out_of_scope(message)
        print(f"User Message: {message}")
        print(f"Assistant Reply: {reply}\n")
