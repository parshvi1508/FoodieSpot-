from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from restaurant.database import session
from restaurant.models import Restaurant, Table, Reservation, User

reservations_bp = Blueprint('reservations', __name__)

@reservations_bp.route('/check_availability', methods=['POST'])
def check_availability():
    try:
        data = request.get_json()
        
        # Extract request data
        restaurant_id = data.get('restaurant_id')
        party_size = data.get('party_size')
        date_str = data.get('date')  # Format: "2025-05-26"
        time_str = data.get('time')  # Format: "19:00"
        
        # Parse datetime
        reservation_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        
        # Find available tables
        available_tables = session.query(Table).filter(
            Table.restaurant_id == restaurant_id,
            Table.capacity >= party_size,
            Table.is_available == True
        ).all()
        
        if available_tables:
            return jsonify({
                'available': True,
                'available_tables': len(available_tables),
                'suggested_table_id': available_tables[0].id
            }), 200
        else:
            return jsonify({'available': False, 'message': 'No tables available'}), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@reservations_bp.route('/make_reservation', methods=['POST'])
def make_reservation():
    try:
        data = request.get_json()
        
        # Extract data
        user_name = data.get('user_name')
        user_phone = data.get('user_phone')
        user_email = data.get('user_email', '')
        restaurant_id = data.get('restaurant_id')
        table_id = data.get('table_id')
        party_size = data.get('party_size')
        date_str = data.get('date')
        time_str = data.get('time')
        
        # Parse datetime
        reservation_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        
        # Check if user exists, create if not
        user = session.query(User).filter_by(phone=user_phone).first()
        if not user:
            user = User(name=user_name, phone=user_phone, email=user_email)
            session.add(user)
            session.commit()
        
        # Create reservation
        reservation = Reservation(
            user_id=user.id,
            restaurant_id=restaurant_id,
            table_id=table_id,
            datetime=reservation_datetime,
            party_size=party_size,
            status='confirmed'
        )
        
        session.add(reservation)
        session.commit()
        
        return jsonify({
            'success': True,
            'reservation_id': reservation.id,
            'message': 'Reservation created successfully'
        }), 201
        
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 400

@reservations_bp.route('/reservation/<int:reservation_id>', methods=['GET'])
def get_reservation(reservation_id):
    try:
        reservation = session.query(Reservation).filter_by(id=reservation_id).first()
        
        if not reservation:
            return jsonify({'error': 'Reservation not found'}), 404
        
        return jsonify({
            'reservation_id': reservation.id,
            'user_name': reservation.user.name,
            'restaurant_name': reservation.restaurant.name,
            'datetime': reservation.datetime.isoformat(),
            'party_size': reservation.party_size,
            'status': reservation.status
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
