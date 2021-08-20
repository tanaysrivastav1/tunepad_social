from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SubmitField, IntegerField
from wtforms.fields import Field
from wtforms.widgets import TextInput
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from web_package.models import User
import uuid


# class TagListField(Field):
#     widget = TextInput()
#     def _value(self):
#         if self.data:
#             return u', '.join(self.data)
#         else:
#             return u''
#     def process_formdata(self, valuelist):
#         if valuelist:
#             self.data = [x.strip() for x in valuelist[0].split(',')]
#         else:
#             self.data = []

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm password', validators=[DataRequired(), EqualTo('password')])
    profile_pic = FileField('profile picuture', validators=[FileAllowed(['png', 'jpg'])])
    submit = SubmitField('register')

    def validate_username(self, username):
        already_used_name = User.query.filter_by(username=username.data).first()
        if already_used_name:
            raise ValidationError(f'someone already use this username')

    def validate_email(self, email):
        already_used_email = User.query.filter_by(email=email.data).first()
        if already_used_email:
            raise ValidationError(f'someone already use this email')

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('login')


#project id textbox
#Flask UUID field form

#auto-increment id for creating posts
class PostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    # tags = TagListField('tag', validators=[DataRequired()])
    project_id = IntegerField('project id', validators=[DataRequired()])
    description = TextAreaField('description')
    artwork = FileField('artwork', validators=[FileAllowed(['png', 'jpg'])])
    submit = SubmitField('post')

    #IntegerField('project id', validators=[DataRequired()])

