from flask import Blueprint, render_template, redirect, url_for, request, session
from models.users import Users
from database import db
from utils.passwords import check_password, hash_password


# Blueprint para o UserController
user_bp = Blueprint('user', __name__)


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Aqui você verifica o usuário e faz o login
        # Exemplo simples:
        user = Users.query.filter_by(username=username).first()
        if user and check_password(password, user.password):
            session['user_id'] = user.id
            return redirect(url_for('main.home'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')


@user_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Adicione o novo usuário ao banco
        new_user = Users(username=username, email=email, password=hash_password(password))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('user.login'))
    
    return render_template('signup.html')


@user_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('user.login'))
