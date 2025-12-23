from flask import Blueprint, request, jsonify
from models import Client, db
from datetime import datetime

clients_bp = Blueprint('clients', __name__)

# Route for adding client
@clients_bp.route('/add', methods=['POST'])
def add_client():
    try:
        # Получаем данные из JSON-запроса
        client_data = request.get_json()

        # Извлекаем данные клиента
        full_name = client_data.get('full_name')
        birth_date_str = client_data.get('birth_date')
        phone_number = client_data.get('phone_number')
        email = client_data.get('email')
        passport_details = client_data.get('passport_details')
        address = client_data.get('address')

        # Преобразуем дату рождения в datetime объект
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')

        # Создаем нового клиента
        new_client = Client(
            full_name=full_name,
            birth_date=birth_date,
            phone_number=phone_number,
            email=email,
            passport_details=passport_details,
            address=address
        )

        # Добавляем клиента в базу данных
        db.session.add(new_client)
        db.session.commit()

        # Возвращаем информацию о добавленном клиенте
        return jsonify({
            "client_id": new_client.client_id,
            "full_name": new_client.full_name,
            "birth_date": new_client.birth_date.strftime('%Y-%m-%d'),
            "phone_number": new_client.phone_number,
            "email": new_client.email,
            "passport_details": new_client.passport_details,
            "address": new_client.address,
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# Route for deleting client
@clients_bp.route('/delete-client/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    try:
        client = Client.query.get(client_id)
        if client:
            db.session.delete(client)
            db.session.commit()
            return jsonify({"message": "Client deleted successfully"}), 200
        else:
            return jsonify({"message": "Client not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500
