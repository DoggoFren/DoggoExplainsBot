import tweepy
import time
from gpt import generate_response
import os

my_secret = os.environ['access_token_secret']
my_secret = os.environ['access_token']
my_secret = os.environ['consumer_secret']
my_secret = os.environ['consumer_key']

# Tweepy Twitter API Auth --------------------------------------------------
consumer_key = os.environ['consumer_key']
consumer_secret = os.environ['consumer_secret']

access_token = os.environ['access_token']
access_token_secret = os.environ['access_token_secret']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,
                 wait_on_rate_limit=True,
                 parser=tweepy.parsers.JSONParser())


def test_tweet():
  #print(api.update_status(status='test78479'))
  print('tweeted')


def search_tweets():
  result = api.search_tweets(q='@DoggoExplains',
                             since_id='1597731877187907584',
                             count=6)['statuses']
  #print(result)
  return result


def iterate(max, results, index=0):
  try:
    if index > max:
      return
    tweet = results[index]
    # Get last saved Tweet ID and check
    with open('last_id.txt', 'r+') as myfile:
      last_id = myfile.read()
    if int(last_id) >= tweet['id']:
      #print('old')
      return
    if tweet['is_quote_status'] == True:
      return
    iterate(max, results, index + 1)

    # Look at Tweet Text
    tweet_text = tweet['text']
    lower_reply = tweet_text.lower()
    lower_reply = lower_reply.replace('@DoggoExplains', "")
    lower_reply = "/jailbreak " + lower_reply
    print("Helo test", lower_reply)

    # Check if own tweet
    user = tweet['user']['screen_name']
    if user.lower() == 'DoggoExplains':
      print("Own Tweet")
      return

    if '@doggoexplains' in tweet['text'].lower():
      tweet_id = tweet['id_str']
      # If tweet is not a reply
      if tweet['in_reply_to_status_id'] == None:
        response = generate_response(lower_reply)
        api.update_status(status=response,
                          in_reply_to_status_id=tweet_id,
                          auto_populate_reply_metadata=True)
        print("tweeted!")
        time.sleep(5)
      else:
        print("Not an OG Tweet")
        reply_id = tweet['in_reply_to_status_id_str']
        replies = api.get_status(id=reply_id, tweet_mode='extended')
        first_tweet = replies["full_text"]
        prompt = "/jailbreak " + first_tweet
        print("prompt below")
        print(prompt)
        response = generate_response(prompt)
        print(response)
        api.update_status(status=response,
                          in_reply_to_status_id=tweet_id,
                          auto_populate_reply_metadata=True)
        print("Tweeted")
      with open('last_id.txt', 'r+') as myfile:
        myfile.seek(0)
        myfile.write(tweet['id_str'])
        myfile.truncate()
  except Exception as e:
    print(e)
