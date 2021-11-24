import tweepy
import variables

def get_tweet(user):
  auth = tweepy.OAuthHandler(variables.TWITTER_API_KEY,variables.TWITTER_SECRET_API_KEY)
  auth.set_access_token(variables.TWITTER_ACCESS_TOKEN,variables.TWITTER_ACCESS_TOKEN_SECRET)  
  api = tweepy.API(auth)
  tweets = api.user_timeline(user)
  how_many_tweets = 1
  finalresult = ""
  for tweet in tweets:
    if(how_many_tweets == 1):
      #print(tweet.text)
      finalresult = tweet.text
      how_many_tweets =- 1
      return finalresult
  return finalresult