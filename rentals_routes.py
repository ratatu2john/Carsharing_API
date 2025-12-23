from flask import Blueprint, request, jsonify
from models import Rental, db
from datetime import datetime

rentals_bp = Blueprint('rentals', __name__)

# Добавление аренды
@rentals_bp.route('/add', methods=['POST'])
def add_rental():
    try:
        # Получаем данные из JSON-запроса
        rental_data = request.get_json()

        # Извлекаем параметры
        user_id = rental_data['user_id']
        car_id = rental_data['car_id']
        rental_start_date = datetime.strptime(rental_data['rental_start_date'], '%Y-%m-%d')
        rental_end_date = datetime.strptime(rental_data['rental_end_date'], '%Y-%m-%d') if rental_data['rental_end_date'] else None
        rental_cost = rental_data['rental_cost']
        tariff_id = rental_data['tariff_id']

        # Создаем новую аренду
        new_rental = Rental(
            user_id=user_id,
            car_id=car_id,
            rental_start_date=rental_start_date,
            rental_end_date=rental_end_date,
            rental_cost=rental_cost,
            tariff_id=tariff_id
        )

        # Сохраняем в базу данных
        db.session.add(new_rental)
        db.session.commit()

        return jsonify({
            "rental_id": new_rental.rental_id,
            "message": "Rental added successfully"
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


# Удаление аренды
@rentals_bp.route('/delete-rental/<int:rental_id>', methods=['DELETE'])
def delete_rental(rental_id):
    try:
        rental = Rental.query.get(rental_id)
        if rental:
            db.session.delete(rental)
            db.session.commit()
            return jsonify({"message": "Rental deleted successfully"}), 200
        else:
            return jsonify({"message": "Rental not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500
