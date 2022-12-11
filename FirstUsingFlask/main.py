from flask import Flask, render_template, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json

with open('static/config.json', 'r') as c:
    params = json.load(c)["params"]

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

# Connecting App to Our Email Account for E-mails
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',   
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['email-username'],
    MAIL_PASSWORD = params['email-password']
    # MAIL PORT can either be 587 or 465
)
mail = Mail(app)


# Connecting to the Table and Fields
class usercredentials(db.Model):
        sno = db.Column(db.Integer(), primary_key = True)
        name = db.Column(db.String(), nullable=False)
        dob = db.Column(db.String(), nullable=False)
        username = db.Column(db.String(30), nullable=False)
        emailid = db.Column(db.String(), unique=True, nullable=False)
        password = db.Column(db.String(), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def signin():
    return render_template('index.html', params=params)

@app.route('/signup', methods=['GET','POST'])
def registration():
    if (request.method == 'POST'):
        # Getting Entries to the Database
        name = request.form.get('userName')
        dob = request.form.get('userDob')
        email = request.form.get('userEmail')
        username = email[0:-10]
        password = request.form.get('userPassword')
        password2 = request.form.get('userPassword2')

        # Adding Entries to the Database
        # While Adding Entries, taking first entry from class and another entry is value from html document
        entry = usercredentials(name=name, dob=dob, username=username, emailid=email, password=password)

        if (password2==password):
            db.session.add(entry)
            db.session.commit()

            mail.send_message(
                'A New Registration From' + name,
                sender = email,
                recipients = [params['email-recepient']],
                body = dob + password,
            )

            # session['user'] = email
            return redirect('/authentication')
        
        else:
            flash("Passwords does not match!")
            return render_template('signup.html', params=params)

    return render_template('signup.html', params=params)


@app.route("/authentication/<string:currentUser>", methods=['GET'])
def authentication(currentUser):
    credentials = usercredentials.query.filter_by(username=currentUser).all()
    return render_template("authentication.html", params=params, credentials=credentials)

@app.route('/home', methods=['GET', 'POST'])
def home():

    return render_template('home.html', params=params)

app.run(debug=True)