# from flask import Blueprint, render_template, request
# from models import Car
# from compile import db

# cars_bp = Blueprint('cars', __name__)

# @cars_bp.route('/')
# def cars_list():
#     # Получить все автомобили из базы данных
#     cars = Car.query.all()
#     return render_template('cars.html', cars=cars)

# @cars_bp.route('/add', methods=['POST'])
# def add_car():
#     mark = request.form['mark']
#     model = request.form['model']
#     status = request.form.get('status', 'available')  # Установить статус по умолчанию
#     new_car = Car(mark=mark, model=model, status=status)
#     db.session.add(new_car)
#     db.session.commit()
#     return 'Car added successfully!'
