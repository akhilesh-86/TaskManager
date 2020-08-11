from .models import User
from helloapp import app, db
from datetime import datetime


def login_user(user, ):
    user = loginUser()
    db_user = User.query.filter_by(name=user.name, pwd=user.pwd)
    
    print (db_user)
    try:
        if (len(db_user) > 0):
            user.is_authenticated = True
            user.is_active = True
            user.is_anonymous = False



