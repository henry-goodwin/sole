from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, RadioField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired

class RegisterForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SellShoes(FlaskForm):
    name = StringField('Shoe Name:',
                        validators=[DataRequired()])
    brand = StringField('Shoe Brand:',
                        validators=[DataRequired()])
    price = IntegerField('Asking Price ($):',
                        validators=[DataRequired(), NumberRange(min=0, max= 100000)])

    condition = RadioField('Condition:', choices=[('New', 'New'), ('Used', 'Used')], validators=[DataRequired()])

    size = SelectField(
            'Shoe Size:',
            choices=[('US Mens 8', 'US Mens 8'), ('US Mens 9', 'US Mens 9'), ('US Mens 10', 'US Mens 10'), ('US Mens 11', 'US Mens 11'), ('US Mens 12', 'US Mens 12'), ('US Mens 13', 'US Mens 13'), ('US Mens 14', 'US Mens 14'), ('US Mens 15', 'US Mens 15'), ('US Mens 16', 'US Mens 16'), ('US Mens 17', 'US Mens 17')],
            validators=[DataRequired()]
        )

    colour_way = StringField('Colour Way:',
                            validators=[DataRequired()])
    description = TextAreaField('Description:',
                            validators=[DataRequired()])
    style = StringField('Style:',
                            validators=[DataRequired()])
    submit = SubmitField('Sell My Shoes')

    image = FileField('Image:', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'])
    ])

class PlaceBid(FlaskForm):
    bid_amount = IntegerField('Bid Amount ($):', validators = [DataRequired()])
    phone_number = StringField('Contact Number:', validators = [DataRequired()])
    submit = SubmitField('Place Bid')

class Search(FlaskForm):
    search = StringField('Search', validators = [DataRequired()])
    submit = SubmitField('Search')

    
