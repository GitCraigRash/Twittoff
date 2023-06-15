from flask_sqlalchemy import SQLAlchemy

# create a DB object form SQLAchemy class

DB = SQLAlchemy()


class User(DB.Model):
    # id column
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    # username column
    username = DB.Column(DB.String, nullable=False)
    # backref is as if we have added a tweets list to the user class.
    # tweets = []
    newest_tweet_id = DB.Column(DB.BigInteger)
    def __repr__(self):
        return f"User: {self.username}"


class Tweet(DB.Model):
    # id column
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    # text column
    text = DB.Column(DB.Unicode(300))
    #vectorizatoin column
    vect = DB.Column(DB.PickleType, nullable = False)
    # user_id column
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'),nullable=False)

    since_id=DB.Column(DB.BigInteger)
    # user column create a two-way link 
    # between a user obejct and a tweeted obejct.
    user = DB.relationship('User', backref=DB.backref('tweets',lazy=True))

    def __repr__(self):
        return f"Tweet: {self.text}"
