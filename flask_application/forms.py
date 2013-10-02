from flask.ext.wtf import Form, TextField, PasswordField, DateField, IntegerField, SelectField
from flask.ext.wtf import Required, Email, EqualTo, Length, validators, URL, Optional

class RegisterForm(Form):
    name = TextField('Username', validators=[Required(), Length(min=3, max=25)])
    email = TextField('Email', validators=[Required(), Length(min=6, max=40)])
    password = PasswordField('Password',
                                validators=[Required(), Length(min=6, max=40)])
    confirm = PasswordField(
                'Repeat Password',
                [Required(), EqualTo('password', message='Passwords must match')])

class LoginForm(Form):
    name = TextField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])

class PostLink(Form):
    #link = TextField('Link',[
                                        #validators.EqualTo(URL(require_tld = True), message='Invalid URL!')
                                        #Length(min=3, max=60))
                                        #])
    #link = TextField('Link', validators=[Optional(), URL(require_tld=False)])
    link = TextField('Group', validators = [Required(), Length(min=1, max=60)])
    group = TextField('Group', validators = [Required(), Length(min=3, max=50)])

class PostGroup(Form):
    group = TextField('Group', validators = [Required(), Length(min=1, max=50)])