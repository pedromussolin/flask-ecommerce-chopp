from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify
from models.users import Users, UsersAddress
from database import db
from utils.passwords import check_password, hash_password
import string
import requests


# Blueprint para o UserController
user_bp = Blueprint('user', __name__)


# Login do usuário
@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Users.query.filter_by(email=email).first()

        if user and check_password(password, user.password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_email'] = user.email

            return redirect(url_for('main.home'))
        
        return render_template('login.html', error="Credenciais inválidas")
    
    return render_template('login.html')


# Cadastrar usuário
@user_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form['full_name'].title()
        first_name = request.form['first_name'].strip().split(' ')[0]
        password = request.form['password']
        email = request.form['email']
        cpf = request.form['cpf'].translate(str.maketrans('', '', string.punctuation))
        phone = request.form['phone'].translate(str.maketrans('', '', string.punctuation))

        # Adicione o novo usuário ao banco
        new_user = Users(full_name=full_name, first_name=first_name, email=email, password=hash_password(password), cpf=cpf, phone=phone)
        db.session.add(new_user)
        db.session.commit()

        street = request.form['street'].title()
        number = request.form['number']
        complement = request.form['complement'].title()
        neighborhood = request.form['neighborhood'].title() 
        state = request.form['state'].title()
        city = request.form['city'].title()
        zip_code = request.form['zip_code'].translate(str.maketrans('', '', string.punctuation))

        # Adicione o endereço do usuário ao banco
        new_address = UsersAddress(user_id=new_user.id, street=street, number=number, complement=complement, neighborhood=neighborhood, city=city, state=state, zip_code=zip_code)
        db.session.add(new_address)
        db.session.commit()

        return redirect(url_for('user.login'))
    
    state_endpoint = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados'
    response = requests.get(state_endpoint)
    states = response.json()

    return render_template('signup.html', states=states)


# Faz o logout do usuário
@user_bp.route('/logout')
def logout():
    session.clear()
    
    return redirect(url_for('user.login'))


# Coleta as cidades de um estado específico
@user_bp.route('/get_cities', methods=['GET'])
def get_cities():
    state_id = request.args.get('state_id')
    cities_url = f'https://servicodados.ibge.gov.br/api/v1/localidades/estados/{state_id}/municipios'
    response = requests.get(cities_url)
    cities = response.json()

    return jsonify(cities)