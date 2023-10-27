from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ProductForm(FlaskForm):
    title = StringField("title", [DataRequired()])
    img_url = StringField('img_url', [DataRequired()])
    description = StringField("description")
    price = StringField('price', [DataRequired()])
    submit = SubmitField()