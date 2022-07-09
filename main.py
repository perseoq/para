from crypt import methods
from turtle import back
from flask import Flask, g, redirect, render_template, request, redirect, url_for, session
from datetime import timedelta
import os
from flask_sqlalchemy import SQLAlchemy
from backend.paradigma import paradise


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://reet:marca666@localhost/paradig2022'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(20)
db = SQLAlchemy(app)

paradigma = paradise()

class Users(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user = db.Column(db.String(300), nullable=False)
    clave = db.Column(db.String(300), nullable=False)

    def __init__(self, user, clave):
        self.user = user
        self.clave = clave

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

@app.route('/')
def index():
    return render_template('home/index.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user', None)
        if request.method == 'POST':
            username = request.form['user_form']
            contrasena = request.form['passwd_form']
            datos = Users.query.filter_by(user=username,clave=contrasena).first()
            if datos:
                session['user'] = request.form['user_form']
                return redirect(url_for('principal'))
    return render_template('home/index.html')

@app.route('/cerrar_sesion')
def cerrar_sesion():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/principal')
def principal():
    if g.user:
        return render_template('home/panel.html', user=session['user'])
    return render_template('home/index.html')


'''
MUESTRA TEXTBOX Y HACE EL RESUMEN
'''

@app.route('/resumen', methods=['GET', 'POST'])
def resumen_paradise():
    if g.user:
        if request.method == 'POST':
            texto = request.form['texto_completo']
            nw = request.form['numero']
            nw = int(nw)
            paradise = paradigma.resumen(texto, nw)
            return render_template('home/resumen.html', paradise=paradise)
        return render_template('home/panel.html', user=session['user'])
    return render_template('home/index.html')
'''
CREA BASE DE DATOS Y EJECUTA FLASK
'''
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)