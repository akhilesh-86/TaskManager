from helloapp import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(500), index=True, nullable=False, primary_key=True)
    status = db.Column(db.String(10), index=True)
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
    type = db.Column(db.String(20), index=True)
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



class UniqueIDs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status_id = db.Column(db.Integer)
    task_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    status_hist_id = db.Column(db.Integer)

