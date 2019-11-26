from wtforms import Form,StringField,TextAreaField,TextField,validators,SubmitField
from wtforms.validators import URL,DataRequired
class urlform(Form):
    url = StringField('url', validators = [DataRequired(), URL()])
    submit = SubmitField('Submit')