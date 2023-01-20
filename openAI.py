import json
import requests
import openai
from time import sleep

class OpenAi:
    def __init__(self,prefix='Im goa'):

        self.api_key = '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'
        self.headers = {
            'authority': 'api.openai.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': 'Bearer sess-B0JOc1QvIF5lKIksUhpBjFupgGOXyqEGN5bNSaBd',
            'content-type': 'application/json',
            'origin': 'https://beta.openai.com',
            'referer': 'https://beta.openai.com/',
            'sec-ch-ua': '"Not_A Brand";v="99", "Microsoft Edge";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.55'
        }
        self.url = "https://api.openai.com/dashboard/user/api_keys"
        self.api_key = self.updateKey()
        self.prefix = prefix

    def getKeys(self):
        response = requests.request("GET", self.url, headers=self.headers)

        return json.loads(response.text)['data']

    def generateKey(self):

        payload = json.dumps({
            "action": "create"
        })

        response = requests.request(
            "POST", self.url, headers=self.headers, data=payload)

        return json.loads(response.text)['key']['sensitive_id']

    def deleteKey(self, sensitive_id, created_at):
        payload = json.dumps({
            "action": "delete",
            "created_at": created_at,
            "redacted_key": sensitive_id,
        })

        response = requests.request(
            "POST", self.url, headers=self.headers, data=payload)
        print(response.text)

    def updateKey(self):
        keys = self.getKeys()
        keys.pop(0)
        print(keys)
        if len(keys) == 0:
            return self.generateKey()
        for key in keys:
            self.deleteKey(key['sensitive_id'], key['created'])

        return self.generateKey()

    def askQuestion(self, question):
        try:
            openai.api_key = self.api_key
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=self.prefix+question,
                temperature=0,
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            return response.choices[0].text
        except:
            sleep(5)
            self.updateKey()
            return self.askQuestion(question)


if __name__ == "__main__":
    openi = OpenAi()
    print(openi.askQuestion('i need you'))
