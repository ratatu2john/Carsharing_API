from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user
from sqlalchemy.sql import text
from compile import db
from models import Client, User, Admin, Support

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/select_role', methods=['GET', 'POST'])
def select_role():
    if request.method == 'POST':
        role = request.form.get('role')
        # Перенаправление на логин в зависимости от роли
        if role == 'admin':
            return redirect(url_for('auth.login_admin'))
        elif role == 'client':
            return redirect(url_for('auth.login_client'))
        elif role == 'support':
            return redirect(url_for('auth.login_support'))
    return render_template('select_role.html')


@auth_bp.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.admin_password == password:  # Проверка без хэширования
            login_user(admin)
            return redirect(url_for('admin.dashboard'))  # Убедитесь, что путь правильный
        flash('Invalid username or password', 'danger')
    return render_template('login.html', role='Admin')


@auth_bp.route('/login_client', methods=['GET', 'POST'])
def login_client():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        client = Client.query.filter_by(user_name=username).first()
        if client and client.password == password:  # Проверка без хэширования
            login_user(client)
            return redirect(url_for('client.dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html', role='Client')


@auth_bp.route('/login_support', methods=['GET', 'POST'])
def login_support():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        support = Support.query.filter_by(user_name=username).first()
        if support and support.password == password:  # Проверка без хэширования
            login_user(support)
            return redirect(url_for('support.support_dashboard'))  
        flash('Invalid username or password', 'danger')
    return render_template('login.html', role='Support')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            # Получение данных из формы
            username = request.form['username']
            password = request.form['password']
            role = request.form['role']
            full_name = request.form.get('full_name', '')
            email = request.form.get('email', '')
            phone = request.form.get('phone', '')

            # Проверка на уникальность имени пользователя
            if role == 'client' and db.session.execute(
                text('SELECT user_name FROM client WHERE user_name = :username'),
                {'username': username}
            ).first():
                flash('Имя пользователя уже используется клиентом!', 'danger')
                return redirect(url_for('auth.register'))

            if role == 'admin' and db.session.execute(
                text('SELECT username FROM admin WHERE username = :username'),
                {'username': username}
            ).first():
                flash('Имя пользователя уже используется администратором!', 'danger')
                return redirect(url_for('auth.register'))

            if role == 'support' and db.session.execute(
                text('SELECT user_name FROM support WHERE user_name = :username'),
                {'username': username}
            ).first():
                flash('Имя пользователя уже используется поддержкой!', 'danger')
                return redirect(url_for('auth.register'))

            # Создание пользователя в зависимости от роли
            if role == 'client':
                birth_date = request.form['birth_date']
                passport_details = request.form['passport_details']
                address = request.form.get('address', '')

                db.session.execute(
                    text('''
                    INSERT INTO client (full_name, birth_date, phone_number, email, passport_details, address, user_name, password)
                    VALUES (:full_name, :birth_date, :phone_number, :email, :passport_details, :address, :username, :password)
                    '''),
                    {
                        'full_name': full_name,
                        'birth_date': birth_date,
                        'phone_number': phone,
                        'email': email,
                        'passport_details': passport_details,
                        'address': address,
                        'username': username,
                        'password': password
                    }
                )

            elif role == 'admin':
                db.session.execute(
                    text('''
                    INSERT INTO admin (username, admin_password, full_name)
                    VALUES (:username, :password, :full_name)
                    '''),
                    {
                        'username': username,
                        'password': password,
                        'full_name': full_name
                    }
                )

            elif role == 'support':
                db.session.execute(
                    text('''
                    INSERT INTO support (user_name, password, full_name, email, phone)
                    VALUES (:username, :password, :full_name, :email, :phone)
                    '''),
                    {
                        'username': username,
                        'password': password,
                        'full_name': full_name,
                        'email': email,
                        'phone': phone
                    }
                )
            else:
                flash('Указана неверная роль!', 'danger')
                return redirect(url_for('auth.register'))

            # Сохранение изменений
            db.session.commit()
            flash(f'Пользователь с ролью {role.capitalize()} успешно создан!', 'success')
            return redirect(url_for('auth.select_role'))

        except Exception as e:
            db.session.rollback()
            flash(f'Произошла ошибка: {e}', 'danger')

    return render_template('register.html')
