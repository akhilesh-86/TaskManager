from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators

# Define QuoteForm below
class QuoteForm(FlaskForm):
  qauthor = StringField("Quotes Author", [validators.Length(min=3,max=100), validators.DataRequired()])
  qstring = StringField("Quotes", [validators.Length(min=3,max=200), validators.DataRequired()])
  submit = SubmitField("Add Quote")
  