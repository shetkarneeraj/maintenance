from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, TimeField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('Data entry operator', 'Data entry operator'), ('Admin', 'Admin'), ('Data analyst', 'Data analyst')], validators=[DataRequired()])
    submit = SubmitField('Register')

class MaintenanceForm(FlaskForm):
    types_of_breakdown = reason = SelectField('Reason', choices=['PROCESS ', 'ELECTRICAL', 'MECHANICAL ', 'RAW MATERIAL SPLITING',
       'CHAIN TRANSFER '], validators=[DataRequired()])
    reason = SelectField('Reason', choices=[
        'BILLET JAM', 'BAR JAM', 'KUNDI BAR JAM', 'PALTI BAR JAM',
        'BAR OUT', 'BOLT LOOSE', 'LOOP BAR JAM', 'PASS CHANGE',
        'PIPE SETTING', 'GUIDE BOX CHANGE', 'GUIDE BOX SETTING',
        'DUE TO THOKAR', 'TMT LINE', 'FISH WIRE BREAK',
        'BEARING FAILURE', 'JOINT BAR JAM', 'SNAP SHEAR WAS DOWN',
        'REHEATING FURNACE', 'BLOCK MILL TRIP', 'LOOPER PROBLEM',
        'STUCK BAR JAM', 'BAR GOES OUT', 'CABLE BURN', 'NUT BOLT LOOSE',
        'CHAIN BROKEN', 'CHILLI STICK', 'CHILLI BAR JAM',
        'SPLIT BAR JAM', 'COOLING BED JAM', 'POWER FAILURE'
    ], validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    breakdown_description = TextAreaField('Breakdown Description', validators=[DataRequired()])
    corrective_action = TextAreaField('Corrective Action to be Taken', validators=[DataRequired()])
    start_time = TimeField('Maintenance Start Time', validators=[DataRequired()])
    end_time = TimeField('Maintenance End Time', validators=[DataRequired()])
    mr = StringField('M.R.', validators=[DataRequired()])
    submit = SubmitField('Submit')
