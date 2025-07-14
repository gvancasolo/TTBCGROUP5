from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, DateField,FloatField
from wtforms.validators import DataRequired, Length, EqualTo,Optional


class LoginForm(FlaskForm):
    username = StringField("შიყვანეთ სახელი", validators=[DataRequired()])
    password = PasswordField("შეიყვანეთ პაროლი", validators=[DataRequired(),Length(min=8, max=12)])
    submit = SubmitField("შესვლა")


class RegistrationForm(FlaskForm):
    username = StringField("შეიყვანე სახელი", validators=[DataRequired()])
    password = PasswordField("შეიყვანე პაროლი", validators=[DataRequired(), Length(min=8, max=12)])
    repeat_password = PasswordField("გაიმეორე პაროლი", validators=[
        DataRequired(), Length(min=8, max=12), EqualTo("password")
    ])
    gender = RadioField("აირჩიე სქესი", choices=["კაცი", "ქალი"], validators=[DataRequired()])
    birthday = DateField("მონიშნე დაბადების თარიღი", format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField("რეგისტრაცია")


class ProductForm(FlaskForm):
    img = FileField("აირჩიე ფოტო", validators=[
    
        FileAllowed(["jpg", "jpeg", "png", "webp"], "მხოლოდ ფოტოები!")
    ])
    name = StringField("სახელი", validators=[DataRequired()])
    price = FloatField("ფასი", validators=[DataRequired()])
    submit = SubmitField("შექმნა")
