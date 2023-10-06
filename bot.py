import openai
import requests
import time
import os
from dotenv import load_dotenv

class TelegramChatBot:
    """Telegram chatbot that answers questions related to Platzi courses and also can recommend them based
    on the provided description or question"""
    def __init__(self, env_file):
        load_dotenv(dotenv_path='./secrets/keys.env')
        self.telegram_token = os.getenv('TELEGRAM_TOKEN')
        self.open_api_key = os.getenv("OPENAI_API_KEY")
        self.model_engine = os.getenv("MODEL_ENGINE")
        openai.api_key = self.open_api_key

    def get_updates(self, offset=None):
        """Retrieve the new messages from the Telegram chat"""
        url = f"https://api.telegram.org/bot{self.telegram_token}/getUpdates"
        params = {"timeout": 100, "offset": offset}
        response = requests.get(url, params=params)
        return response.json()["result"]

    def send_message(self, chat_id, text):
        """Send a message to the chat, answering on behalf of chatbot"""
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        params = {"chat_id":chat_id, "text":text}
        response = requests.post(url=url, params=params)
        return response

    def get_openai_response(self, prompt):
        """Send requests to OpenAI fine-tuned model with the user question provided to the chatbot"""
        try:
            response = openai.Completion.create(
                engine = self.model_engine,
                prompt = prompt+"-> ",
                max_tokens = 200,
                n = 1,
                stop = ["END"],
                temperature = 0.3
            )
            return response["choices"][0]["text"].strip()

        except openai.error.APIError as e:
            # Manejar error de API aquí, p. reintentar o iniciar sesión
            print(f"La API de OpenAI devolvió un error de API: {e}")
            pass# Aprobar
        except openai.error.APIConnectionError as e:
            # Manejar error de conexión aquí
            print(f"Error al conectarse a la API de OpenAI: {e}")
            pass
        except openai.error.RateLimitError as e:
            # Manejar error de límite de tasa (recomendamos usar retroceso exponencial)
            print(f"La solicitud de API de OpenAI excedió el límite de frecuencia: {e}")
            pass
        return "Ocurrio un error"

    def run(self):
        """Run the chatbot and keep receiving messages"""
        print("Starting bot...")
        offset = 0
        while True:
            updates = self.get_updates(offset=offset)
            if updates:
                for update in updates:
                    offset = update["update_id"] + 1
                    chat_id = update["message"]["chat"]["id"]
                    user_message = update["message"]["text"]
                    if user_message == '/start':
                        continue
                    print(f"Message received: {user_message}")
                    gpt = self.get_openai_response(user_message)
                    print(f"Answer generated: {gpt}")
                    self.send_message(chat_id, gpt)
            else:
                time.sleep(1)

if __name__ == '__main__':
    chatbot = TelegramChatBot(env_file='/.secrets/keys.env')
    chatbot.run()
