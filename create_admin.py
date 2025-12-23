from flask import Blueprint, request, jsonify
from models import Client, db  # Импортируем модель Client и объект db для работы с БД

# Создаем Blueprint для маршрутов с клиентами
clients_bp = Blueprint('clients', __name__)

# Маршрут для добавления нового клиента
@clients_bp.route('/add-client', methods=['POST'])
def add_client():
    full_name = request.form.get('full_name')
    birth_date = request.form.get('birth_date')
    phone_number = request.form.get('phone_number')
    email = request.form.get('email')
    passport_details = request.form.get('passport_details')
    address = request.form.get('address')

    new_client = Client(
        full_name=full_name,
        birth_date=birth_date,
        phone_number=phone_number,
        email=email,
        passport_details=passport_details,
        address=address
    )

    db.session.add(new_client)
    db.session.commit()

    return jsonify({"client_id": new_client.client_id, "full_name": new_client.full_name, "birth_date": new_client.birth_date}), 201

# Маршрут для удаления клиента
@clients_bp.route('/delete-client/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    client = Client.query.get(client_id)
    
    if client:
        db.session.delete(client)
        db.session.commit()
        return jsonify({"message": "Client deleted successfully", "client_id": client_id}), 200
    else:
        return jsonify({"message": "Client not found"}), 404
