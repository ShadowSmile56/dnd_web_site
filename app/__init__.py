from flask_login import LoginManager
from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_object(Config)

app.config['SQLALCHEMY_DATABASE_URI'] = ""
Dnd = SQLAlchemy(app)
migrate = Migrate(app, Dnd)
title='Dnd'

login = LoginManager(app)
login.login_view = 'login'

'''
if __name__ == '__main__':
   #create table
   Dnd.create_all()
   Dnd.init_app(app)


# remember to turn app debug by setting it to false in production
   app.run(debug=True)
'''
from app import routes, models

'''# psycopg2
engine = create_engine('postgresql+psycopg2://postgres:15780@localhost:5432/dnd')
engine.connect()'''



