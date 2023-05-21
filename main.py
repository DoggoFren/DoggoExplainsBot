import os
import openai

openai.api_key = os.environ['OPENAI_API_KEY']
import time
import schedule
from keep_alive import keep_alive
from twitter_functions import search_tweets, iterate, test_tweet
from gpt import generate_response

max = 5


def main():
  try:
    tweets = search_tweets()
    iterate(max, tweets)
  except Exception as e:
    print(e)


keep_alive()
main()

schedule.every(55).seconds.do(main)

while 1:
  schedule.run_pending()
  time.sleep(1)
