from flask import Flask, render_template
from .models import DB,User,Tweet

def create_app():

    app = Flask(__name__)
    # database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite3'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
    
    # Register aour dtabas ewith teha pp
    DB.init_app(app)

    my_var="Twitoff App"

    @app.route('/')
    def root():
        users = User.query.all()
        
        return render_template("base.html",title="Home", users=users)

    @app.route('/bananas')
    def bananas():
        return "This is the bananas page"

    @app.route('/reset')
    def reset():
        # drop database tables
        DB.drop_all()
        # Recreate all database tables accordint tothe
        # indicate shema in models.py
        DB.create_all()
        return "dabase has been reset "
    @app.route('/populate')
    def populate():
        ryan = User(id=1, username='ryan')
        DB.session.add(ryan)
        julian = User(id=2, username='julian')
        DB.session.add(julian)

        #tweets
        tweet1 = Tweet(id=1, text= "ryan's tweet text", user=ryan)
        DB.session.add(tweet1)
        tweet2 = Tweet(id=2, text= "julian's tweet text", user=julian)
        DB.session.add(tweet2)
        # save changes to dtabase
        DB.session.commit()

        return "database has been populated"
    return app
