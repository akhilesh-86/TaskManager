from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, DateTimeField, RadioField, SelectField, PasswordField

# Define QuoteForm below
class QuoteForm(FlaskForm):
  qauthor = StringField("Quotes Author", [validators.Length(min=3,max=100), validators.DataRequired()])
  qstring = StringField("Quotes", [validators.Length(min=3,max=200), validators.DataRequired()])
  submit = SubmitField("Add Quote")

class TaskForm(FlaskForm):
  currTime = DateTimeField("Current Time")
  action = RadioField("Select Action", choices=["Add Task","Update Task", "Delete Task"])
  taskName = StringField("Task Description(New)", [validators.Length(min=5,max=500)])
  taskList = SelectField("Select Task to Update") # choices will be updated dynamically
  submit = SubmitField("Submit")
  getTask = SubmitField("Get Task List")

class UserForm(FlaskForm):
  currTime = DateTimeField("Current Time")
  action = RadioField("Select Action", choices=["Add User","Update User Password", "Delete User"])
  userName = StringField("User Name", [validators.Length(min=2,max=50)])
  password = PasswordField("Password")
  userList = SelectField("Select User to Update") # choices will be updated dynamically
  submit = SubmitField("Submit")
  getUser = SubmitField("Get User List")
  reset = SubmitField("Reset")