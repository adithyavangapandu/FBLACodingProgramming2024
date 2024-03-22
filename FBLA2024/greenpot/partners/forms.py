from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, HiddenField, DecimalField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Optional, Email, ValidationError


class PartnerForm(FlaskForm):
    PartnerName = StringField('Partner Name',validators=[DataRequired()])
    ContactEmail = StringField('Contact Email')
    ContactIndividual = StringField('Contact Individual')
    PhoneNumber = StringField('Phone Number')
    PartnerType = SelectField('Partner Type', choices=[('Business', 'Business'), ('Community', 'Community')],
                              validators=[DataRequired()])
    Resources = TextAreaField('Resources', validators=[DataRequired()])
    submit = SubmitField('Submit')
    Money = DecimalField('Money', validators=[NumberRange(min=0, message="Please enter a valid amount of money.")])
    NumTime = IntegerField('NumTime', validators=[NumberRange(min=None, max=None, message="Please enter a valid integer.")])
    Timeframe = SelectField('Timeframe', choices=[('day', 'Day'), ('week', 'Week'), ('month', 'Month'), ('year', 'Year')])
    Responsibilities = TextAreaField('Responsibilities', validators=[DataRequired()])


class NotificationForm(FlaskForm):
    reminder_type = SelectField('Reminder Type', choices=[
        ('payment', 'Payment Reminder'), 
        ('responsibilities', 'Responsibilities Reminder'),
        ('custom', 'Custom Reminder')
    ], validators=[DataRequired()])
    custom_message = TextAreaField('Custom Message (Optional)')
    partner_id = HiddenField('Partner ID', default='', validators=[DataRequired()])  # Stores the partner's ID for association
    submit = SubmitField('Create Reminder')