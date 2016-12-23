from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

DATABASE = 'my_data'
PASSWORD = 'asdfghjkl'
USER = 'root'
HOSTNAME = 'localhost'


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s/%s'%(USER, PASSWORD, HOSTNAME, DATABASE)
db = SQLAlchemy(app)

class Example1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=False)
    email = db.Column(db.String(200), unique=False)
    category = db.Column(db.String(200), unique=False)
    description = db.Column(db.String(200), unique=False)
    link = db.Column(db.String(200), unique=False)
    estimated_costs = db.Column(db.String(200), unique=False)
    submit_date = db.Column(db.String(200), unique=False)
    status = db.Column(db.String(200), unique=False)
    decision_date = db.Column(db.String(200), unique=False)


    def __init__(self, id, name, email, category, description, link, estimated_costs, submit_date, status, decision_date):

        self.id=id
        self.name=name
        self.email=email
        self.category=category
        self.description = description
        self.link = link
        self.estimated_costs = estimated_costs
        self.submit_date = submit_date
        self.status = status
        self.decision_date = decision_date

def createDatabase():
    import sqlalchemy
    temp = sqlalchemy.create_engine('mysql://%s:%s@%s'%(USER, PASSWORD, HOSTNAME))
    temp.execute("CREATE DATABASE IF NOT EXISTS %s"%(DATABASE))

if __name__ == '__main__':
    app.run()
