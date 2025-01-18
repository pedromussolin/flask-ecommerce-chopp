from flask import Blueprint, render_template, redirect, url_for, session

# Blueprint para o MainController
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return redirect(url_for('main.home'))

@main_bp.route('/home')
def home():
    name = session.get('name', None)
    
    return render_template('home.html', name=name)

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/help')
def help():
    return render_template('help.html')


