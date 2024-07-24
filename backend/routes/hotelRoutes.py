from flask import Blueprint,jsonify,request
from .models import Hotel
from bson import ObjectId

hotels_blueprint = Blueprint('hotels', __name__)

#Fech Hotels

@hotels_blueprint.route('/api/hotels', methods=['GET'])
def get_data():
    hotels = Hotel.objects.all()
    transformed_hotels = []

    for hotel in hotels:
        transformed_hotel = {
            'id': str(hotel.id),  # Convert ObjectId to string
            'hotel_name':hotel.hotel_name,
            'district':hotel.district,
            'state':hotel.state,
            'landmark':hotel.landmark
        }
        transformed_hotels.append(transformed_hotel)

    return jsonify(transformed_hotels), 200

#Add Hotels
@hotels_blueprint.route('/api/hotels', methods=['POST'])
def add_hotel():
    data = request.json
    hotel = Hotel(**data)
    try:
        hotel.save()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    # Return success response
    return jsonify({'message': 'Hotel added successfully'}), 201

#Delete Hotel
@hotels_blueprint.route('/api/hotels/<string:hotel_id>', methods=['DELETE'])
def delete_room(hotel_id):
    try:
        hotel_id = ObjectId(hotel_id)
    except Exception as e:
        return jsonify({'error': 'Invalid hotel ID format'}), 400  # Bad Request
    
    # Find the hotel by ID
    hotel = Hotel.objects(id=hotel_id).first()

    # Check if the room exists
    if not hotel:
        return jsonify({'error': 'Hotel not found'}), 404  # Not Found

    # Delete the room from the database
    try:
        hotel.delete()
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Internal Server Error
    
    # Return success response
    return jsonify({'message': 'Hotel deleted successfully','status':200}), 200
