from flask import Blueprint, request, jsonify
from models import Maintenance, db  # Импортируем модель Maintenance и db

maintenance_bp = Blueprint('maintenance', __name__)

# Маршрут для добавления записи обслуживания
@maintenance_bp.route('/add', methods=['POST'])
def add_maintenance():
    try:
        data = request.form  # Используем form для получения данных из формы
        car_id = data.get('car_id')
        maintenance_date = data.get('maintenance_date')
        maintenance_type = data.get('maintenance_type')
        status = data.get('status')
        notes = data.get('notes')

        if not car_id or not maintenance_date or not maintenance_type or not status:
            return jsonify({"message": "Missing required fields"}), 400

        # Создаем и добавляем запись в базу данных
        new_maintenance = Maintenance(
            car_id=car_id,
            maintenance_date=maintenance_date,
            maintenance_type=maintenance_type,
            status=status,
            notes=notes
        )
        db.session.add(new_maintenance)
        db.session.commit()

        return jsonify({"id": new_maintenance.maintenance_id, "message": "Maintenance added successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# Маршрут для удаления записи обслуживания
@maintenance_bp.route('/delete-maintenance/<int:maintenance_id>', methods=['DELETE'])
def delete_maintenance(maintenance_id):
    try:
        # Ищем запись по ID
        maintenance = Maintenance.query.get(maintenance_id)
        if maintenance:
            db.session.delete(maintenance)
            db.session.commit()
            return jsonify({"message": "Maintenance record deleted successfully", "maintenance_id": maintenance_id}), 200
        else:
            return jsonify({"message": "Maintenance record not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Маршрут для получения всех записей обслуживания
@maintenance_bp.route('/get-maintenance', methods=['GET'])
def get_maintenance():
    try:
        maintenances = Maintenance.query.all()
        result = [
            {
                "maintenance_id": maintenance.maintenance_id,
                "car_id": maintenance.car_id,
                "maintenance_date": maintenance.maintenance_date,
                "maintenance_type": maintenance.maintenance_type,
                "status": maintenance.status,
                "notes": maintenance.notes
            } for maintenance in maintenances
        ]
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500
