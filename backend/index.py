from flask import Flask
from routes.roomRoutes import rooms_blueprint
import pymongo
from mongoengine import connect
from routes.userLogin import user_blueprint
from routes.hotelRoutes import hotels_blueprint
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your_secret_key'

MONGODB_URI = "mongodb+srv://hotel-management-app:hotel-management-app@cluster0.vuus3rz.mongodb.net/"
DATABASE_NAME = "hotel-management-app"

# Connect to MongoDB
try:
    client = pymongo.MongoClient(MONGODB_URI)
    db = client[DATABASE_NAME]
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    db = None

# Connect mongoengine to the MongoDB instance
connect(db=DATABASE_NAME, host=MONGODB_URI)

# Register the blueprint
app.register_blueprint(rooms_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(hotels_blueprint)

if __name__ == '__main__':
    app.run(debug=True, port=5000)