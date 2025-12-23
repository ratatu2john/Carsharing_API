from flask import Blueprint, render_template
from models import Car, Client, Rental, Payment, Maintenance, Tariff

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
def dashboard():
    cars = Car.query.all()  # Получаем все автомобили
    clients = Client.query.all()  # Получаем всех клиентов
    rental = Rental.query.all()  # Получаем все аренды
    payments = Payment.query.all()  # Получаем все платежи
    maintenances = Maintenance.query.all()  # Получаем все технические обслуживания
    tariffs = Tariff.query.all()  # Получаем все тарифы

    return render_template('admin_dashboard.html')

@admin_bp.route('/manage-users')
def manage_users():
    clients = Client.query.all()  # Получаем всех клиентов
    return render_template('manage_users.html', clients=clients)


@admin_bp.route('/manage-cars')
def manage_cars():
    cars = Car.query.all()  # Получаем все автомобили
    return render_template('manage_cars.html', cars=cars)


@admin_bp.route('/manage_maintenance')
def manage_maintenance():
    maintenances = Maintenance.query.all()
    return render_template('manage_maintenance.html', maintenances=maintenances)

@admin_bp.route('/manage_rentals')
def manage_rentals():
   rentals = Rental.query.all()
   return render_template('manage_rentals.html', rentals=rentals)


@admin_bp.route('/manage-tariffs')
def manage_tariffs():
    tariffs = Tariff.query.all()  # Получаем все тарифы
    return render_template('manage_tariffs.html', tariffs=tariffs)


@admin_bp.route('/manage-payments')
def manage_payments():
    payments = Payment.query.all()  # Получаем все платежи
    return render_template('manage_payments.html', payments=payments)
