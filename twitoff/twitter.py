'''Handles connection to NotTiwtter API using NotTweepy'''

from os import getenv
import not_tweepy.user as tweepy
import spacy
from twitoff.models import DB, Tweet, User

# Get API Key from environment vars.
key = getenv('TWITTER_API_KEY')
secret = getenv('TWITTER_API_KEY_SECRET')

# Connect to the Twitter API
TWITTER_AUTH = tweepy.OAuthHandler(key, secret)
TWITTER = tweepy.API(TWITTER_AUTH)


def add_or_update_user(username):
    '''Takes username and pulls user from Twitter API'''
    twitter_user = TWITTER.get_user(screen_name=username)
    # Is there a user in the database that already has this id?
    # If not, then create a User in the database with this id.
    db_user = (User.query.get(twitter_user.id)) or User(id=twitter_user.id, username=username)

    # add the user to the database.
    DB.session.add(db_user)

    # get the user's tweets
    tweets = twitter_user.timeline(count=200, 
                                   exclude_replies=True, 
                                   include_rts=False, 
                                   tweet_mode='extended')

    # add each tweet to the database
    for tweet in tweets:
        db_tweet = Tweet(id=tweet.id,
                         text=tweet.full_text[:300],
                         user_id=db_user.id)
        db_user.tweets.append(db_tweet)
        DB.session.add(db_tweet)

    # Save the changes to the DB
    DB.session.commit()
    