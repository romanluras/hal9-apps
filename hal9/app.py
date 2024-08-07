from groq import Groq
import os
import hal9 as h9

prompt = input("")
h9.event('prompt', prompt
)
context = open('context.txt', 'r').read()

messages = h9.load("messages", [{"role": "system", "content": context}])
messages.append({"role": "user", "content": prompt})

stream = Groq().chat.completions.create(model = "llama3-70b-8192", messages = messages, temperature = 0, seed = 1, stream = True)

response = ""
for chunk in stream:
  if len(chunk.choices) > 0 and chunk.choices[0].delta.content is not None: 
    print(chunk.choices[0].delta.content, end="")
    response += chunk.choices[0].delta.content

messages.append({"role": "assistant", "content": response})

h9.save("messages", messages, hidden=True)
