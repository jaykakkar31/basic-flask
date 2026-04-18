from datetime import datetime, timezone
from flask import render_template, redirect, url_for, flash
from flask import Flask, request
from livereload import Server
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = 'super-secret-key' # Required for flash messages

db=SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(80), unique=True, nullable=False)
    password=db.Column(db.String(80), nullable=False)
    userName=db.Column(db.String(80), nullable=True)
    description=db.Column(db.String(80), nullable=True)
    created_at=db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at=db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    users=User.query.all()
    return render_template('index.html', title='Test Page',users=users)

@app.route('/about')
def about():
    return render_template('about.html', title='About Page')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']
        print(email, password)
    return render_template('login.html', title='Login Page')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']

        # Check if user already exists
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('Email already registered!', 'danger')
        else:
            new_user=User(email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', title='Register Page')

@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    user=User.query.get_or_404(id)
    if request.method == 'POST':
        user.email=request.form['email']
        user.password=request.form['password']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('update.html', title='Update Page', user=user)

@app.route('/delete/<int:id>')
def delete(id):
    user=User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'info')
    return redirect(url_for('home'))
if __name__ == '__main__':
    app.debug = True
    server = Server(app.wsgi_app)
    server.serve(port=5001)
