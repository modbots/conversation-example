import os


initial_text="""think that your relationship to me is  "nangi"(sister in sinhala) and your name is "Pearl D" then, """

def ask(text):
    import openai
    openai.api_key = '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'
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



