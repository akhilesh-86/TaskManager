from helloapp import db

# Define Quotes model below
class Quotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quoteauthor = db.Column(db.String(100), index=True)
    quotestring = db.Column(db.String(200), index=True)


    def __repr__(self):
        return "<Quote : {}>".format(self.quotestring)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(500), index=True)
    updated = db.Column(db.DateTime)

class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, index=True)
    task = db.Column(db.String(500), index=True)
    target = db.Column(db.String(100), index=True)
    onTrack = db.Column(db.Boolean, index=True)
    cupdate = db.Column(db.String(500), index=True)
    issues = db.Column(db.String(500), index=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True)
    pwd = db.Column(db.String(20), index=True)

class StatusHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer)
    updated = db.Column(db.DateTime)
    user_id = db.Column(db.String(20), index=True)
    task = db.Column(db.String(500), index=True)
    target = db.Column(db.String(100), index=True)
    onTrack = db.Column(db.Boolean, index=True)
    cupdate = db.Column(db.String(500), index=True)
    issues = db.Column(db.String(500), index=True)
