import json
import os

from dotenv import load_dotenv
from flask import Flask, render_template, redirect, request, session, \
    url_for, flash

from .data_base import employee_authentication, clients_by_employee, \
    edit_client_data
from .utils import gen_password

app = Flask('__name__')
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
app.secret_key = SECRET_KEY


@app.get('/')
def client_list():
    limit = int(request.values.get("limit", 10))
    page = int(request.values.get("page", 1))
    order = request.values.get("order")

    if 'user' not in session:
        return redirect(url_for('login'), 302)

    employee_name = session['user']['name']

    clients, paginator = clients_by_employee(employee_name, limit, page, order)
    return render_template(
        'pages/client_list.html',
        clients_list=map(dict, clients),
        paginator=paginator
    )


@app.put("/clients/<string:client_id>")
def edit_client(client_id):
    new_data = json.loads(request.data)
    employee_name = session['user']['name']
    edit_client_data(employee_name, client_id, new_data)
    return {"message": "data updated"}, 200


@app.route('/login/', methods=['GET', 'POST'])
def login():

    if 'user' in session:
        return redirect(url_for('client_list'), 302)

    if request.method == 'GET':
        return render_template('pages/login.html')

    form_data = dict(request.form)
    user_login = form_data['login']
    user_password = form_data['password']

    if not user_login or not user_password:
        flash('Все поля должны быть заполнены', 'danger')
        return render_template('pages/login.html')

    user = employee_authentication(user_login, gen_password(user_password))

    if not user:
        flash('Не верный логин/пароль', 'danger')
        return render_template('pages/login.html')

    session['user'] = dict(user)

    return redirect(url_for('client_list'))


@app.post('/logout/')
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect(url_for('login'))
