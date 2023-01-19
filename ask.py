import os
import openai


initial_text="""think that your relationship to me is  "nangi"(sister in sinhala) and your name is "Pearl D" then, """

openai.api_key = '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'
def ask(text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=initial_text+text,
        temperature=0,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response.choices[0].text

if __name__== '__main__':
    print(ask('nangi what is your iop ?'))



