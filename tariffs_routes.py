from flask import Blueprint, request, jsonify
from models import Tariff, db  # Импортируем модель Tariff и объект db для работы с БД

# Создаем Blueprint для маршрутов с тарифами
tariffs_bp = Blueprint('tariffs', __name__)

# Маршрут для добавления нового тарифа
@tariffs_bp.route('/add', methods=['POST'])
def add_tariff():
    name = request.form.get('name')
    cost_per_minute = request.form.get('cost_per_minute')
    cost_per_hour = request.form.get('cost_per_hour')
    conditions = request.form.get('conditions')

    new_tariff = Tariff(
        name=name,
        cost_per_minute=cost_per_minute,
        cost_per_hour=cost_per_hour,
        conditions=conditions
    )

    db.session.add(new_tariff)
    db.session.commit()

    return jsonify({"tariff_id": new_tariff.tariff_id, "name": new_tariff.name, "cost_per_minute": new_tariff.cost_per_minute}), 201

# Маршрут для удаления тарифа
@tariffs_bp.route('/delete/<int:tariff_id>', methods=['DELETE'])
def delete_tariff(tariff_id):
    tariff = Tariff.query.get(tariff_id)
    
    if tariff:
        db.session.delete(tariff)
        db.session.commit()
        return jsonify({"message": "Tariff deleted successfully", "tariff_id": tariff_id}), 200
    else:
        return jsonify({"message": "Tariff not found"}), 404
