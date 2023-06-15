'''Handles connection to NotTiwtter API using NotTweepy'''

from os import getenv
import spacy
import not_tweepy as tweepy
from .models import DB, Tweet, User

# Get API Key from environment vars.
key = getenv('TWITTER_API_KEY')
secret = getenv('TWITTER_API_KEY_SECRET')

# Connect to the Twitter API
TWITTER_AUTH = tweepy.OAuthHandler(key, secret)
TWITTER = tweepy.API(TWITTER_AUTH)


def add_or_update_user(username):
    '''Takes username and pulls user from Twitter API'''
    try:
        twitter_user = TWITTER.get_user(screen_name=username)
        # Is there a user in the database that already has this id?
        # If not, then create a User in the database with this id.
        #print(twitter_user.user_data)
        db_user = (User.query.get(twitter_user.screen_name)) or User(id=twitter_user.screen_name, username=username)

        # add the user to the database.
        DB.session.add(db_user)

        # get the user's tweets
        
        tweets = twitter_user.timeline(count=200, 
                                    exclude_replies=True, 
                                    include_rts=False, 
                                    tweet_mode='extended')
        
        
        
        # add each tweet to the database
        for tweet in tweets:
            tweet_vector = vectorize_tweet(tweet.full_text)
            db_user.newest_tweet_id = tweets[0].id
            db_tweet = Tweet(id=tweet.id,
                             text=tweet.full_text[:300],
                             user_id=db_user.id,
                             vect = tweet_vector,
                             since_id=db_user.newest_tweet_id)
        if tweets:
            db_user.newest_tweet_id = tweets[0].id
            DB.session.add(db_tweet)
        

    except Exception as e:
        print(f"Error Processing {username}: {e}")
        raise e
    else:
        # Save the changes to the DB
        DB.session.commit()

nlp = spacy.load('my_model/')
#We have the same too we used in the flask shell
def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector
