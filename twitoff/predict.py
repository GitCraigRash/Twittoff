from sklearn.linear_model import LogisticRegression
import numpy as np 
from .models import User 
from .twitter import vectorize_tweet


def predict_user(user0_username,user1_username, hypo_tweet_text):
    
    #Grab the users from the DB
    user0 = User.query.filter(User.username==user0_username).one()
    user1 = User.query.filter(User.username==user1_username).one()

    # Get the word embeddings from each user
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    # vertially stack the two 2D numpy arrays to make our X matrix
    X_train = np.vstack([user0_vects, user1_vects])

    # concatinate our labels of 0 or 1 for each tweet
    zeros = np.zeros(user0_vects.shape[0])
    ones = np.ones(user0_vects.shape[0])

    y_train = np.concatenate([zeros, ones])

    # Instantiate and fit a logistic regression model
    log_reg = LogisticRegression().fit(X_train,y_train)

    # vecotrize the hypothetical tweet text
    # make sure it's held in a 2D numpy array rather than 1D
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text).reshape(1, -1)

    return log_reg.predict(hypo_tweet_vect)[0]

    '''
    Hello! I am in Sprint 11 module 3. I have written the predict_user() function as in the video but when I add, say, elonmusk and common_squirrel, and try to predict them with predict_user('elonmusk','common_squirrel','We are sending astronauts to space with rockets'), I receive an error saying NameError: name 'user0' is not defined. When looking the problem up, it seems that the user0_username in predict_user(user0_username,user1_username, hypo_tweet_text) is undefined.'''