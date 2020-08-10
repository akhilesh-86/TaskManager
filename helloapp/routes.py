from flask import render_template, request, redirect, url_for
import random
from .models import UniqueIDs
from .models import Task
from .models import User
from .models import Status
from .forms import TaskForm
from .forms import StatusUpdateForm
from .forms import UserForm
from .forms import StatusForm
from helloapp import app, db
from datetime import datetime

@app.route('/')
def hello():
    return render_template('index.html')

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
                  id_db = UniqueIDs.query.all()
                  if (len(id_db) == 0):
                      i = UniqueIDs(id=1, task_id=1, status_id=1)
                      db.session.add(i)
                      db.session.commit()
                      id = 1
                      status_id=1
                  else:
                      if (id_db[0].task_id == None):
                          id = 1
                      else:
                          id = int(id_db[0].task_id)+1

                      print (id_db[0].status_id)
                      if (id_db[0].status_id == None):
                          status_id = 1
                      else:
                          status_id = int(id_db[0].status_id)+1

                      i = UniqueIDs.query.filter_by(id=id_db[0].id).update(dict(task_id=id,status_id=status_id))
                      db.session.commit()

                  task = Task(id=id,updated = datetime.now(),task=form.taskName.data,status=form.status.data)
                  db.session.add(task)
                  db.session.commit()
                  task1 = Task.query.filter_by(updated=task.updated)[0]
                  status = Status(id=status_id,task_id=task1.id,task=task1.task,onTrack=True)
                  db.session.add(status)
                  db.session.commit()
                  return render_template('manage_tasks.html', form=form, message="Task Added Successfully", field=None, ctime = datetime.now(), db_task=db_task_list)

          elif (str(form.action.data) == "Update Task"):
             if (form.status.data is None or len(str(form.status.data)) == 0):
                  field  = "Status"
                  err = "Please select Status"
                  return render_template('manage_tasks.html', form=form, err=err, field=field, ctime = datetime.now(), db_task=db_task_list)

             if (form.taskName.data is None or len(str(form.taskName.data)) == 0):
                  field = "TaskList"
                  err = "Please update proper descriptio of the Task to Update"
                  return render_template('manage_tasks.html', form=form, err=err, field=field, ctime = datetime.now(), db_task=db_task_list)

             if (form.taskList.data is None or len(str(form.taskList.data)) == 0):
                  field = "TaskList"
                  err = "Please select task from list to Update"
                  return render_template('manage_tasks.html', form=form, err=err, field=field, ctime = datetime.now(), db_task=db_task_list)
             l = Task.query.filter_by(task=str(form.taskName.data))
             try:
                print (l[0])
                found=True
             except:
                found=False
             if (found == True and str(form.taskList.data) != str(form.taskName.data)):
                  field = "TaskName"
                  err = "Task Already Exists"
                  return render_template('manage_tasks.html', form=form, err=err, field=field, ctime = datetime.now(), db_task=db_task_list)

             task = Task.query.filter_by(task=str(form.taskList.data)).update(dict(task=str(form.taskName.data),status=str(form.status.data)))
             db.session.commit()
             return render_template('manage_tasks.html', form=form, message="Task Updated Successfully", field=None, ctime = datetime.now(), db_task=db_task_list)

          elif (str(form.action.data) == "Delete Task"):
             if (len(str(form.taskList.data)) == 0 or form.taskList.data is None):
                  field = "TaskList"
                  err = "Please select task from list to Delete"
                  return render_template('manage_tasks.html', form=form, err=err, field=field, ctime = datetime.now(), db_task=db_task_list)

             task = Task.query.filter_by(task=str(form.taskList.data))
#             status = Status.query.filter_by(task_id=task[0].id)
#             try:
#                 db.session.delete(status[0])
#             except:
#                 print ("Skipped")
             db.session.delete(task[0])
             db.session.commit()
             return render_template('manage_tasks.html', form=form, message="Task DeletedSuccessfully", field=None, ctime = datetime.now(), db_task=db_task_list)
             
      elif (form.getTask.data):
          db_task_list = Task.query.all()
          if (len(db_task_list) == 0):
              return render_template('manage_tasks.html', form=form, ctime = datetime.now(), db_task=db_task_list, message="No records found")

          task_list = [task.task for task in Task.query.all()]
          form.taskList.choices = task_list
          form.taskName.data = task_list[0]
          form.status.data = ""
          return render_template('manage_tasks.html', form=form, ctime = datetime.now(), db_task=db_task_list)

  task = Task.query.all()
  try:
      form.taskList.choices = [task.task for task in Task.query.all()]
  except:
      form.taskList.choices = []
  return render_template('manage_tasks.html', form=form, ctime = datetime.now(), db_task=task)
 



@app.route('/user/', methods=['GET', 'POST'])
def manage_users():
  form = UserForm()
  if (request.method == 'POST'):
      db_user=User.query.all()
      if (form.submit.data):
          if (not form.action.data):
              field  = "Action"
              err = "Please select Action"
              return render_template('manage_users.html', form=form, err=err, field=field, ctime = datetime.now(),user=db_user)

          elif (str(form.action.data) == "Add User"):

              if (form.userName.data is None or len(str(form.userName.data)) > 50 or len(str(form.userName.data)) < 2):
                  field  = "UserName"
                  err = "UserName Must be between 2-50 characters"
                  return render_template('manage_users.html', form=form, err=err, field=field, ctime = datetime.now(),user=db_user)

              elif (len(str(form.userName.data).split()) > 1 ):
                  field  = "UserName"
                  err = "UserName Must not contain space"
                  return render_template('manage_users.html', form=form, err=err, field=field, ctime = datetime.now(),user=db_user)

              elif (form.userType.data is None):
                  field  = "UserType"
                  err = "Please select UserType"
                  return render_template('manage_users.html', form=form, err=err, field=field, ctime = datetime.now(),user=db_user)

              else:
                  user = User(name=form.userName.data,pwd=form.password.data,type=form.userType.data)
                  db.session.add(user)
                  db.session.commit()
                  return render_template('manage_users.html', form=form, message="User Added Successfully", field=None, ctime = datetime.now(),user=db_user)

          elif (str(form.action.data) == "Update User Password"):
             user = User.query.filter_by(name=str(form.userList.data)).update(dict(pwd=str(form.password.data)))
             db.session.commit()
             return render_template('manage_users.html', form=form, message="Password Updated Successfully", field=None, ctime = datetime.now(),user=db_user)

          elif (str(form.action.data) == "Delete User"):
             user = User.query.filter_by(name=str(form.userList.data))
             db.session.delete(user[0])
             db.session.commit()
             return render_template('manage_users.html', form=form, message="User Deleted Successfully", field=None, ctime = datetime.now(),user=db_user)
             
      elif (form.getUser.data):

#          if (str(form.action.data) == "Update User Password" or str(form.action.data) == "Delete User"):
#              form.userName.render_kw = {'disabled': 'disabled'}

          user_list = [user.name for user in User.query.all()]
          form.userList.choices = user_list
          return render_template('manage_users.html', form=form, ctime = datetime.now(),user=db_user)

      elif (form.reset.data):
          form = UserForm()
          return render_template('manage_users.html', form=form, ctime = datetime.now(),user=db_user)

  db_user=User.query.all()
  try:
      form.userList.choices = [user.name for user in User.query.all()]
  except:
      form.userList.choices = []
  return render_template('manage_users.html', form=form, ctime = datetime.now(),user=db_user)
 


@app.route('/status/', methods=['GET', 'POST'])
def manage_status():
  form = StatusForm()
  db_task = Task.query.all()
  status = []
  for task in db_task:
      if (task.status == "Open"):
          db_status = Status.query.filter_by(task_id = task.id)
          status.append(db_status[0])
  
  if (request.method == 'POST'):
      for id in request.form:
          task_id = id
          break

      return redirect(url_for('update_status', id=task_id, ctime = datetime.now()))

  return render_template('manage_status.html', form=form, ctime = datetime.now(), db_status=status)
 

@app.route('/status/update/<int:id>', methods=['GET', 'POST'])
def update_status(id):
  form = StatusUpdateForm()
  status =  Status.query.filter_by(task_id=id)[0]
  try:
      if (request.method == 'POST'):
          if (form.back.data):
              return redirect(url_for('manage_status'))
          elif (len(form.cupdate.data) < 1):
              err = "Please provide Proper Status of Task"
              form.id.data = status.id
              form.id.render_kw = {'disabled': 'disabled'}
              form.task_id.data = status.task_id
              form.task_id.render_kw = {'disabled': 'disabled'}
              form.task.data = status.task
              form.task.render_kw = {'disabled': 'disabled'}
              form.target.data = status.target
              form.cupdate.data = status.cupdate
              form.issue.data = status.issues
              return render_template('update_status.html', form=form, ctime = datetime.now(), db_status=status, err=err)
          elif (form.onTrack.data == None):
              err= "Please update if task is on track or not"
              form.id.data = status.id
              form.id.render_kw = {'disabled': 'disabled'}
              form.task_id.data = status.task_id
              form.task_id.render_kw = {'disabled': 'disabled'}
              form.task.data = status.task
              form.task.render_kw = {'disabled': 'disabled'}
              form.target.data = status.target
              form.cupdate.data = status.cupdate
              form.issue.data = status.issues
              return render_template('update_status.html', form=form, ctime = datetime.now(), db_status=status, err=err)
          elif (form.onTrack.data == "Yes"):
            status = True
          elif (form.onTrack.data == "No"):
            status = False
          status_r = Status.query.filter_by(task_id=id).update(dict(target=form.target.data,onTrack=status,cupdate=form.cupdate.data,issues=form.issue.data))
          db.session.commit()
          return redirect(url_for('manage_status'))

      form.id.data = status.id
      form.id.render_kw = {'disabled': 'disabled'}
      form.task_id.data = status.task_id
      form.task_id.render_kw = {'disabled': 'disabled'}
      form.task.data = status.task
      form.task.render_kw = {'disabled': 'disabled'}
      form.target.data = status.target
      form.cupdate.data = status.cupdate
      form.issue.data = status.issues
      return render_template('update_status.html', form=form, ctime = datetime.now(), db_status=status)
  except:
      err = "Some Error Occured... Please try again by closing this window..!"
      form.id.data = status.id
      form.id.render_kw = {'disabled': 'disabled'}
      form.task_id.data = status.task_id
      form.task_id.render_kw = {'disabled': 'disabled'}
      form.task.data = status.task
      form.task.render_kw = {'disabled': 'disabled'}
      form.target.data = status.target
      form.cupdate.data = status.cupdate
      form.issue.data = status.issues
      return render_template('update_status.html', form=form, ctime = datetime.now(), db_status=status, err=err)

