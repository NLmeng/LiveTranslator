import json
import uuid
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class CustomGPT:
    """
    A Python class for interacting with GPT-4 models using the OpenAI API.

    :param model: The model to use for generating the response
    :type model: str, e.g. "gpt-4", "text-davinci-003", "text-davinci-002", ...

    EXAMPLE USAGE:
    if __name__ == "__main__":
        gpt = CustomGPT()
        session = gpt.start_new_chat()
    """

    def __init__(self, model="gpt-4"):
        # Initialize the class with the specified GPT model (default is "gpt-4")
        self.model = model
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
            "content-type": "application/json",
            "Host": "chat.openai.com",
            "origin": "https://chat.openai.com/chat",
            "referer": "https://chat.openai.com/chat",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
        })
        self.session.cookies.set("_puid", os.getenv("_PUID"))
        self.prev_id = str(uuid.uuid4())
        self.fetch_puid()

    def start_new_chat(self):
        """
        Start a new chat session and continuously prompt the user for input.
        Print the model's responses and continue until "exit" is entered.
        """
        res = self.session.post(
            "https://chat.openai.com/backend-api/conversation",
            json={
                "id": str(uuid.uuid4()),
                "model": self.model,
                "action": "next",
                "messages": [],
                "parent_message_id": self.prev_id,
            },
        )
        filtered_data = self.filter_response(res)

        while True:
            user_input = input("message > ")
            if user_input.lower() == "exit":
                break
            response = self.chat(user_input, filtered_data)
            print(response['message']['content']['parts'][0])
            filtered_data = response

    def chat(self, msg, session):
        """
        Send a message (msg) to the GPT-4 model and receive a response.
        Pass the current conversation session as an argument.

        :param msg: The text message to send to the GPT-4 model
        :type msg: str
        :param session: The current conversation session
        :type session: dict
        :return: The model's response as a dictionary
        """
        res = self.session.post(
            "https://chat.openai.com/backend-api/conversation",
            json = {
                "id": str(uuid.uuid4()), 
                "model": self.model,
                "action": "next", 
                "messages": [
                    {
                        "author": {
                            "role": "user"
                        },
                        "role": "user",
                        "content": {
                            "content_type": "text",
                            "parts": [f"{msg}\n"]
                        }
                    }
                ],
                "parent_message_id": session['message']['id'],
                "conversation_id": session['conversation_id'],
            },
        )
        return self.filter_response(res)
    
    def fetch_puid(self):
        """
        Fetch and set the "_puid" cookie for the session.
        """
        res = self.session.get(
            "https://chat.openai.com/backend-api/models",
            headers={
                "key": "value",
            },
        )
        self.session.cookies.set("_puid", res.cookies["_puid"])

    def filter_response(self, res):
        """
        Filter the API response to extract the relevant data.

        :param res: The raw API response
        :type res: requests.Response
        :return: The filtered API response as a dictionary
        """
        non_mt_res = os.linesep.join([txt for txt in res.text.splitlines() if txt])
        data = non_mt_res.splitlines()[len(non_mt_res.splitlines()) - 2]
        filtered_data = json.loads(data[data.find("data: ") + 6:])
        return filtered_data