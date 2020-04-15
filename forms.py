# stocksys/forms.py

from wtforms import StringField, PasswordField, Form,SubmitField,TextField
from wtforms.validators import DataRequired, Email

class EmailPasswordForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class SearchForm(Form):
    autocomp = TextField('Part No', id='parts_autocomplete')
    autocomp1 = TextField('Description', id='desc_autocomplete')
    autocomp2 = TextField('Order Code', id='code_autocomplete')
    submit = SubmitField('Show')


class AddPart(Form):
    part_no = StringField('PART No', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    supplier = StringField('Supplier', id='supp1_autocomplete', validators=[DataRequired()])
    order_code = StringField('Order Code', validators=[DataRequired()])
    cost_price = StringField('Cost Price', validators=[DataRequired()])
    delivered_price = StringField('Delivered Price')
    stock = StringField('Stock', validators=[DataRequired()])
    unit = StringField('Unit')
    lead_time = StringField('Lead Time')
    location = StringField('Location', validators=[DataRequired()])
    reorder_qty = StringField('Reorder Quantity')
    supplier2 = StringField('Supplier 2', id='supp2_autocomplete')
    order_code2 = StringField('Order Code 2')
    submit = SubmitField('Add')
