import tweepy
import datetime
import matplotlib.pyplot as plt
import matplotlib
import math

def main():

  # Authorization
  consumer_key = ""
  consumer_secret = ""
  access_token = ""
  access_token_secret = ""
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)
  api = tweepy.API(auth)

  # Variables for @ and number of tweets to examine
  username = ""
  tweet_count = 1000

  # Retrieve tweets and store in all_tweets
  all_tweets = []
  tweets = api.user_timeline(screen_name = username, count = min(200, tweet_count))
  tweet_count = tweet_count - 200
  all_tweets.extend(tweets)

  # Have to retrieve tweets 200 at a time (tweepy limit)
  while tweet_count > 0:
    tweets = api.user_timeline(screen_name = username, count = min(200, tweet_count), max_id = all_tweets[-1].id - 1)
    all_tweets.extend(tweets)
    tweet_count = tweet_count - 200
  print(str(len(all_tweets)) + " tweets found.")

  # Get tweet times and convert from datetime to float (also converted to CST from UTC)
  tweet_times = []
  for tweet in all_tweets:
    tweet_times.append(tweet.created_at)
  times = matplotlib.dates.date2num(tweet_times)
  hour_times = (math.floor(((time % 1) * 24 - 6) % 24) for time in times)

  # Initialize time categories and count frequency for each hour
  x = range(24)
  y = [0] * 24
  for h in hour_times:
    y[h] += 1

  # Plot graph and lazily label the x-ticks
  plt.bar(x, y)
  plt.xlabel("Time")
  plt.ylabel("Tweet Frequency")
  xticks = []
  for i in range(12):
    if i == 0:
      i = 12
    xticks.append(str(i) + "AM")
  for i in range(12):
    if i == 0:
      i = 12
    xticks.append(str(i) + "PM")
  plt.xticks(range(24), xticks)
  plt.title("Tweet Frequency for " + username + " vs. Hour of Day")
  plt.show()

main()