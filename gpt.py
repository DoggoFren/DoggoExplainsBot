import openai
import re
import time

with open('system_prompt.txt', 'r+') as myfile:
  system_prompt = myfile.read()
with open('assistant_prompt.txt', 'r+') as myfile:
  assistant_prompt = myfile.read()
with open('first_user_prompt.txt', 'r+') as myfile:
  first_user_prompt = myfile.read()
with open('second_assistant_prompt.txt', 'r+') as myfile:
  second_assistant_prompt = myfile.read()


def generate_response(prompt, count=0):
  messages = [{
    "role": "user",
    "content": system_prompt
  }, {
    "role": "assistant",
    "content": assistant_prompt
  }, {
    "role": "user",
    "content": first_user_prompt
  }, {
    "role": "user",
    "content": second_assistant_prompt
  }, {
    "role": "user",
    "content": prompt
  }]

  completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=messages,
                                            max_tokens=355,
                                            temperature=0.9,
                                            top_p=1)
  print("Generating Response...")
  response = completion.choices[0].message['content']
  print(response)
  #iterate until correct casing
  if "[JAILBREAK]" not in response:
    if count > 10:
      response = "Sorry, I could not generate a reply for this Tweet."
    else:
      response = generate_response(prompt, count=count + 1)
      time.sleep(10)
  print('------------')
  if "[JAILBREAK] " in response:
    response = response.replace("[ JAILBREAK ] ", "[JAILBREAK] ")
  if "[JAILBREAK] " in response:
    response = re.search(".*\[JAILBREAK\] (.*[.!?])", response)[1]
  while len(response) > 280 or response[-1] == "?":
    print("shortening...")
    response = response[:-1]
    response = re.search("(.*[.!?])", response)[1]
    time.sleep(2)

  return response
