from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Car, Rental, Payment, Tariff, Client

client_bp = Blueprint('client', __name__)

@client_bp.route('/dashboard')
@login_required
def dashboard():
    # Для клиента отображаем все его аренды и платежи
    print(current_user)
    return render_template('client_dashboard.html')

@client_bp.route('/view-cars')
@login_required
def view_cars():
    cars = Car.query.filter_by(status='доступен').all()  # Получаем только доступные автомобили
    return render_template('view_avaliable_cars.html', cars=cars)

@client_bp.route('/view-payments')
@login_required
def view_payments():
    # Проверяем, является ли текущий пользователь клиентом
    if isinstance(current_user, Client):
        # Получаем все платежи для текущего клиента
        payments = Payment.query.join(Rental, Payment.rental_id == Rental.rental_id) \
                                 .filter(Rental.client_id == current_user.client_id) \
                                 .all()
    else:
        # Для администраторов можно добавить логику для просмотра всех платежей
        payments = Payment.query.all()

    return render_template('view_my_payments.html', payments=payments)

@client_bp.route('/view-tariffs')
@login_required
def view_tariffs():
    tariffs = Tariff.query.all()  # Получаем все тарифы
    return render_template('view_tariffs.html', tariffs=tariffs)
