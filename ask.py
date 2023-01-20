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
    print(ask('nangi what is whats ur age ?'))



