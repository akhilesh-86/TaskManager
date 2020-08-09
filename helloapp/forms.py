from flask_wtf import FlaskForm
from wtforms.widgets import TextArea
from wtforms import StringField, SubmitField, validators, DateTimeField, RadioField, SelectField, PasswordField, BooleanField, IntegerField


class TaskForm(FlaskForm):
  currTime = DateTimeField("Current Time")
  action = RadioField("Select Action", choices=["Add Task","Update Task", "Delete Task"])
  status = RadioField("Task Status", choices=["Open","Close","Pending","Postponed"])
  taskName = StringField("Task Description", [validators.Length(min=5,max=500)], widget=TextArea())
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



class StatusForm(FlaskForm):
  taskName = StringField("Task Description(New)", [validators.Length(min=5,max=500)])
  target = StringField("Target Description", widget=TextArea())
  status = BooleanField("Task Status")
  currentUpdate = StringField("Current Status", widget=TextArea())
  issues = StringField("Issues Related to Task", widget=TextArea())
 
class StatusUpdateForm(FlaskForm):
  id = IntegerField("Task Status ID")
  task_id = IntegerField("Task ID")
  task = StringField("Task Description", widget=TextArea())
  target = StringField("Target Description", widget=TextArea())
  onTrack = RadioField("On Track", choices=["Yes","No"])
  cupdate = StringField("Current Update", widget=TextArea())
  issue = StringField("Issues", widget=TextArea())
  submit = SubmitField("Submit")
  back = SubmitField("Back")


