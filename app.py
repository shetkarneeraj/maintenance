from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from forms import LoginForm, RegistrationForm, MaintenanceForm
from models import db, User, Maintenance
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

def calculate_duration(start_time, end_time):
    start_seconds = start_time.hour * 3600 + start_time.minute * 60 + start_time.second
    end_seconds = end_time.hour * 3600 + end_time.minute * 60 + end_time.second
    return (end_seconds - start_seconds)//60


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@app.route('/home')
@login_required
def home():
    today = datetime.today().date()
    maintenances = Maintenance.query.filter_by(date=today).all()

    maintenance_types = Maintenance.query.with_entities(Maintenance.types_of_breakdown).distinct().all()

    # Prepare the date filter (greater than the 1st of this month)
    first_day_of_month = datetime(datetime.today().year, datetime.today().month, 1)

    # Count frequency for each maintenance type
    maintenance_type_count = {}
    for maintenance_type in maintenance_types:
        maintenance_type = maintenance_type[0]
        count = Maintenance.query.filter(Maintenance.types_of_breakdown == maintenance_type, Maintenance.date >= first_day_of_month).count()
        maintenance_type_count[maintenance_type] = count
    output = []
    for maintenance in maintenances:
        maintenance = maintenance.serialize()
        output.append({
            "type": maintenance["types_of_breakdown"],
            "corrective_action": maintenance["corrective_action"],
            "duration": maintenance["duration"],
            "date": maintenance["date"],
            "name": maintenance["reason"],
            "start_time": maintenance["start_time"].split()[1],
            "end_time": maintenance["end_time"].split()[1],
            "y": [maintenance["start_time"], maintenance["end_time"]],
        })
    return render_template('home.html', maintenances=output,
                           maintenance_type_count={"keys": list(maintenance_type_count.keys()), "values": list(maintenance_type_count.values())})


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'Welcome {user.username}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/maintenance', methods=['GET', 'POST'])
@login_required
def maintenance():
    form = MaintenanceForm()

    if form.validate_on_submit():
        maintenance_record = Maintenance(
            types_of_breakdown=form.types_of_breakdown.data,
            reason=form.reason.data,
            date=form.date.data,
            duration=calculate_duration(form.start_time.data, form.end_time.data),
            breakdown_description=form.breakdown_description.data,
            corrective_action=form.corrective_action.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            mr=form.mr.data,
            user_id=current_user.id
        )
        db.session.add(maintenance_record)
        db.session.commit()
        flash('Maintenance record has been created!', 'success')
        return redirect(url_for('home'))

    return render_template('maintenance_form.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
