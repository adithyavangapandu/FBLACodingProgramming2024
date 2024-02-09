from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, HiddenField
from wtforms.validators import DataRequired


class PartnerForm(FlaskForm):
    PartnerName = StringField('Partner Name',validators=[DataRequired()])
    ContactEmail = StringField('Contact Email')
    ContactIndividual = StringField('Contact Individual')
    PhoneNumber = StringField('Phone Number')
    PartnerType = SelectField('Partner Type', choices=[('Business', 'Business'), ('Community', 'Community')],
                              validators=[DataRequired()])
    Resources = TextAreaField('Resources', validators=[DataRequired()])
    submit = SubmitField('Submit')
    from_page = HiddenField()