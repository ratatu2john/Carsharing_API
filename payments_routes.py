from flask import Blueprint, request, jsonify
from models import Payment, db
from datetime import datetime

payments_bp = Blueprint('payments', __name__)

@payments_bp.route('/add', methods=['POST'])
def add_payment():
    try:
        payment_data = request.get_json()
        rental_id = payment_data.get('rental_id')
        payment_date_str = payment_data.get('payment_date')  # Expecting date and time
        payment_amount = payment_data.get('payment_amount')
        status = payment_data.get('status')

        if not rental_id or not payment_date_str or not payment_amount or not status:
            return jsonify({"message": "Missing required fields"}), 400

        # Convert date string to datetime object
        payment_date = datetime.strptime(payment_date_str, '%Y-%m-%dT%H:%M')

        new_payment = Payment(
            rental_id=rental_id,
            payment_date=payment_date,
            payment_amount=float(payment_amount),
            status=status
        )

        db.session.add(new_payment)
        db.session.commit()

        return jsonify({
            "payment_id": new_payment.payment_id,
            "rental_id": new_payment.rental_id,
            "payment_date": new_payment.payment_date.strftime('%Y-%m-%d %H:%M'),
            "payment_amount": new_payment.payment_amount,
            "status": new_payment.status
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@payments_bp.route('/payment/delete-payment/<int:payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    payment = Payment.query.get(payment_id)
    if payment:
        db.session.delete(payment)
        db.session.commit()
        return jsonify({"message": "Payment deleted successfully"}), 200
    return jsonify({"message": "Payment not found"}), 404


