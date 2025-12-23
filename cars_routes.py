from flask import Blueprint, request, jsonify
from models import Car, db

cars_bp = Blueprint('cars', __name__)

@cars_bp.route('/add', methods=['POST'])
def add_car():
    data = request.form
    new_car = Car(
        mark=data.get('mark'),
        model=data.get('model'),
        year=data.get('year'),
        number=data.get('number'),
        status=data.get('status'),
        geoposition=data.get('geoposition'),
        mileage=data.get('mileage')
    )
    db.session.add(new_car)
    db.session.commit()
    return jsonify({"id": new_car.id}), 201

@cars_bp.route('/delete-car/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    car = Car.query.get(car_id)
    
    if car:
        db.session.delete(car)
        db.session.commit()
        return jsonify({"message": "Car deleted successfully", "car_id": car_id}), 200
    else:
        return jsonify({"message": "Car not found"}), 404


