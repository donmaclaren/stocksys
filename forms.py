# stocksys/forms.py

from wtforms import StringField, PasswordField, Form,SubmitField,TextField
from wtforms.validators import DataRequired, Email

class EmailPasswordForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class SearchForm(Form):
    autocomp = TextField('Select Part No', id='parts_autocomplete')
    submit = SubmitField('Select')


class AddPart(Form):
    part_no = StringField('PART No', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    supplier = StringField('Supplier', validators=[DataRequired()])
    order_code = StringField('Order Code', validators=[DataRequired()])
    cost_price = StringField('Cost Price', validators=[DataRequired()])
    delivered_price = StringField('Delivered Price', validators=[DataRequired()])
    stock = StringField('Stock', validators=[DataRequired()])
    lead_time = StringField('Lead Time', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    reorder_qty = StringField('Reorder Quantity', validators=[DataRequired()])
    supplier2 = StringField('Supplier 2', validators=[DataRequired()])
    order_code2 = StringField('Order Code 2', validators=[DataRequired()])
    submit = SubmitField('Add')
