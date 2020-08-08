from flask import render_template, request
import random
from .models import Task
from .models import User
from .models import Status
from .models import Quotes
from .forms import QuoteForm
from .forms import TaskForm
from .forms import StatusUpdateForm
from .forms import UserForm
from .forms import StatusForm
from helloapp import app, db
from datetime import datetime

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/hello/<string:username>/')
def hello_user(username):

    quotes = Quotes.query.all()
    quotes = [ quote.quotestring for quote in quotes]

    random_quote = random.choice(quotes)

    return render_template('hello_user.html', username=username, quote=random_quote)

@app.route('/quotes/')
def display_quotes():

    quotes = Quotes.query.all()
    quotes = [ quote.quotestring for quote in quotes]

    return render_template('quotes.html', quotes=quotes)

## Define below a view function 'add_quote', which renders 'addquote.html' template that displays the form , QuoteForm
## The form takes a quote and it's author information and submit's it to server.
## The server process the input data and if found valid, the data is inserted into quotes table.
## and finally renders 'addquote_confirmation.html' template.
## In case if any error is found in input, it renders 'addquote.html' template highlighting errors.
## that displays all the quotes present in 'quotes' list in a unordered list.

@app.route('/addquote/', methods=['GET', 'POST'])
def add_quote():
  form = QuoteForm()
  if (request.method == 'POST'):
    qa = len(str(form.qauthor.data))
    qs = len(str(form.qstring.data))
    if (qa == 0):
      return render_template("addquote.html", form=form, field="author", err="[This field is required.]")
    elif (qa < 3 or qa > 100):
      return render_template("addquote.html", form=form, field="author", err="[Field must be between 3 and 100 characters long.]")
    elif (qs == 0):
      return render_template("addquote.html", form=form, field="string", err="[This field is required.]")
    elif (qs < 3 or qs > 200):
      return render_template("addquote.html", form=form, field="string", err="[Field must be between 3 and 200 characters long.]")
    else:
      q1 = Quotes(quoteauthor=form.qauthor.data, quotestring=form.qstring.data)
      db.session.add(q1)
      db.session.commit()
      return render_template("addquote_confirmation.html")

  return render_template("addquote.html", form=form, field=None, err=None)


@app.route('/task/', methods=['GET', 'POST'])
def manage_tasks():
  form = TaskForm()
  if (request.method == 'POST'):
      db_task_list = Task.query.all()
      if (form.submit.data):
          if (not form.action.data):
              field  = "Action"
              err = "Please select Action"
              return render_template('manage_tasks.html', form=form, err=err, field=field, ctime = datetime.now(), db_task=db_task_list )

          elif (str(form.action.data) == "Add Task"):
              if (len(str(form.taskName.data)) > 500 or len(str(form.taskName.data)) < 10 or form.taskName.data is None):
                  field  = "TaskName"
                  err = "Task Must be between 10-500 characters"
                  return render_template('manage_tasks.html', form=form, err=err, field=field, ctime = datetime.now(), db_task=db_task_list)
              elif (form.status.data is None):
                  field  = "Status"
                  err = "Please select Status"
                  return render_template('manage_tasks.html', form=form, err=err, field=field, ctime = datetime.now(), db_task=db_task_list)
              else:
                  task = Task(updated = datetime.now(),task=form.taskName.data,status=form.status.data)
                  db.session.add(task)
                  db.session.commit()
                  task1 = Task.query.filter_by(updated=task.updated)[0]
                  status = Status(task_id=task1.id,task=task1.task,onTrack=True)
                  db.session.add(status)
                  db.session.commit()
                  return render_template('manage_tasks.html', form=form, message="Task Added Successfully", field=None, ctime = datetime.now(), db_task=db_task_list)

          elif (str(form.action.data) == "Update Task"):
             if (len(str(form.status.data)) == 0):
                  field  = "Status"
                  err = "Please select Status"
                  return render_template('manage_tasks.html', form=form, err=err, field=field, ctime = datetime.now(), db_task=db_task_list)

             task = Task.query.filter_by(task=str(form.taskList.data)).update(dict(task=str(form.taskName.data),status=str(form.status.data)))
             db.session.commit()
             return render_template('manage_tasks.html', form=form, message="Task Updated Successfully", field=None, ctime = datetime.now(), db_task=db_task_list)

          elif (str(form.action.data) == "Delete Task"):
             task = Task.query.filter_by(task=str(form.taskList.data))
             status = Status.query.filter_by(task_id=task[0].id)
             try:
                 db.session.delete(status[0])
             except:
                 print ("Skipped")
             db.session.delete(task[0])
             db.session.commit()
             return render_template('manage_tasks.html', form=form, message="Task DeletedSuccessfully", field=None, ctime = datetime.now(), db_task=db_task_list)
             
      elif (form.getTask.data):
          task_list = [task.task for task in Task.query.all()]
          form.taskList.choices = task_list
          form.taskName.data = ""
          form.status.data = ""
          return render_template('manage_tasks.html', form=form, ctime = datetime.now(), db_task=db_task_list)

  return render_template('manage_tasks.html', form=form, ctime = datetime.now(), db_task=[])
 



@app.route('/user/', methods=['GET', 'POST'])
def manage_users():
  form = UserForm()
  if (request.method == 'POST'):
      if (form.submit.data):
          if (not form.action.data):
              field  = "Action"
              err = "Please select Action"
              return render_template('manage_users.html', form=form, err=err, field=field, ctime = datetime.now())

          elif (str(form.action.data) == "Add User"):

              if (len(str(form.userName.data)) > 50 or len(str(form.userName.data)) < 2):
                  field  = "UserName"
                  err = "UserName Must be between 2-50 characters"
                  return render_template('manage_users.html', form=form, err=err, field=field, ctime = datetime.now())
              else:
                  user = User(name=form.userName.data,pwd=form.password.data)
                  db.session.add(user)
                  db.session.commit()
                  return render_template('manage_users.html', form=form, message="User Added Successfully", field=None, ctime = datetime.now())

          elif (str(form.action.data) == "Update User Password"):
             user = User.query.filter_by(name=str(form.userList.data)).update(dict(pwd=str(form.password.data)))
             db.session.commit()
             return render_template('manage_users.html', form=form, message="Password Updated Successfully", field=None, ctime = datetime.now())

          elif (str(form.action.data) == "Delete User"):
             user = User.query.filter_by(name=str(form.userList.data))
             db.session.delete(user[0])
             db.session.commit()
             return render_template('manage_users.html', form=form, message="User Deleted Successfully", field=None, ctime = datetime.now())
             
      elif (form.getUser.data):

#          if (str(form.action.data) == "Update User Password" or str(form.action.data) == "Delete User"):
#              form.userName.render_kw = {'disabled': 'disabled'}

          user_list = [user.name for user in User.query.all()]
          form.userList.choices = user_list
          return render_template('manage_users.html', form=form, ctime = datetime.now())

      elif (form.reset.data):
          form = UserForm()
          return render_template('manage_users.html', form=form, ctime = datetime.now())

  return render_template('manage_users.html', form=form, ctime = datetime.now())
 


@app.route('/status/', methods=['GET', 'POST'])
def manage_status():
  form = StatusForm()
  status =  Status.query.all()
  if (request.method == 'POST'):
      task_id = int(request.form[0])
      print (task_id)
      return redirect(url_for('update_status', id=task_id, ctime = datetime.now()))

  return render_template('manage_status.html', form=form, ctime = datetime.now(), db_status=status)
 

@app.route('/status/update/<int:id>', methods=['GET', 'POST'])
def update_status(id):
  form = StatusUpdateForm()
  status =  Status.query.filter_by(task_id=id)[0]
  form.id.data = status.id
  form.task_id.data = status.task_id
  form.task.data = status.task
  form.target.data = status.target
  form.onTrack.data = status.onTrack
  form.cupdate.data = status.cupdate
  form.issue.data = status.issues
  if (request.method == 'POST'):
      status_r = Status.query.filter_by(task_id=id).update(dict(target=form.target.data,onTrack=form.on_track.data,cupdate=form.cupdate.data,issue=form.issue.data))
      db.session.commit()
      return redirect(url_for('manage_status'))

  return render_template('update_status.html', form=form, ctime = datetime.now(), db_status=status)
