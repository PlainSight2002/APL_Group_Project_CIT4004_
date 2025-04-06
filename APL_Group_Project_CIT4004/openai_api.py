'''
Authors
Sassania Hibbert 1901201
Darrell King 1803342
Shavar Mclean 1903893
Mark Vernon 1908916
Jelani Jackson 1901811
'''

import openai


def chat_with_gpt(prompt, model="gpt-4o-2024-08-06", temperature=0.7):
    api_key = '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'
    openai.api_key = api_key

    response = openai.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )

    return response.choices[0].message.content
