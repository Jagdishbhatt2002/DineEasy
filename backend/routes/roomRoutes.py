from flask import Blueprint, jsonify, request
from .models import Room
from bson import ObjectId

rooms_blueprint = Blueprint('rooms', __name__)

#Fech Rooms
@rooms_blueprint.route('/api/rooms', methods=['GET'])
def get_data():
    rooms = Room.objects.all()
    transformed_rooms = []

    for room in rooms:
        transformed_room = {
            'id': str(room.id),  # Convert ObjectId to string
            'room_no': room.room_no,
            'status': room.status,
            'condition':room.condition,
            'hotel_id':room.hotel_id
        }
        transformed_rooms.append(transformed_room)

    return jsonify(transformed_rooms), 200

#Fetch Room By ID

@rooms_blueprint.route('/api/room-by-id/<room_id>', methods=['GET'])
def get_room(room_id):
    try:
        room = Room.objects.get(id=ObjectId(room_id))
        return jsonify({
            'id': str(room.id),  # Convert ObjectId to string
            'room_no': room.room_no,
            'status': room.status,'condition':room.condition,
            'customer_name': room.customer_name,
            'customer_mobile': room.customer_mobile,
            'booked_from': room.booked_from,
            'booked_till': room.booked_till,
            'booking_price':room.booking_price,
            'booking_purpose':room.booking_purpose,
        }), 200
    except Room.DoesNotExist:
        return jsonify({'message': 'Room not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#Fetch Room by hotel id
@rooms_blueprint.route('/api/hotel-room/<hotel_id>', methods=['GET'])
def fetch_room_by_id(hotel_id):
    rooms = Room.objects(hotel_id=hotel_id)

    transformed_rooms = []
    for room in rooms:
        transformed_room = {
            'id': str(room.id),
            'room_no': room.room_no,
            'status': room.status,
            'condition': room.condition,
            'hotel_id': room.hotel_id
        }
        transformed_rooms.append(transformed_room)

    return jsonify(transformed_rooms), 200

#Add Room
@rooms_blueprint.route('/api/hotels/rooms/<hotel_id>', methods=['POST'])
def add_room(hotel_id):
    data = request.json
    room = Room(**data)
    room.hotel_id = hotel_id
    try:
        room.save()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return jsonify({'message': 'Room added successfully'}), 201

#Delete Room
@rooms_blueprint.route('/api/rooms/<string:room_id>', methods=['DELETE'])
def delete_room(room_id):
    print(type(room_id))
    try:
        room_id = ObjectId(room_id)
    except Exception as e:
        return jsonify({'error': 'Invalid room ID format'}), 400  # Bad Request
    
    print("Converted room_id:", type(room_id))

    # Find the room by ID
    room = Room.objects(id=room_id).first()
    print("Query result:", room)

    # Check if the room exists
    if not room:
        return jsonify({'error': 'Room not found'}), 404  # Not Found

    # Delete the room from the database
    try:
        room.delete()
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Internal Server Error
    
    # Return success response
    return jsonify({'message': 'Room deleted successfully','status':200}), 200

#Update Room
@rooms_blueprint.route('/api/update_room/<room_id>', methods=['PUT'])
def update_room(room_id):
    try:
        data = request.get_json()
        if not ObjectId.is_valid(room_id):
            return jsonify({'error': 'Invalid room_id'}), 400
        room = Room.objects(id=room_id).first()
        if room:
            room.update(**data)
            return jsonify({'message': 'Room updated successfully'}), 200
        else:
            return jsonify({'error': 'Room not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500