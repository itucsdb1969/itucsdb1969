from wtforms import Form, StringField, TextAreaField, PasswordField, SelectField, validators



class LoginForm(Form):
    username = StringField('', [validators.Length(min=4, max=25)])
    email = StringField('', [validators.Length(min=4, max=50)])


class RegisterForm(Form):
    username = StringField('', [validators.Length(min=4, max=25)])
    email = StringField('', [validators.Length(min=4, max=50)])
    password = PasswordField('', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords dont match')
    ])
    confirm = PasswordField('')
