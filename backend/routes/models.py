from mongoengine import Document, StringField, IntField, BooleanField, DateTimeField, EmailField

#Model for user login
class LoginUser(Document):
    email = EmailField(required=True, regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    password = StringField(required=True)

    meta = {'collection': 'loginUser'}

#Model for room
class Room(Document):
    room_no = StringField(required=True)
    status = StringField(required=True, choices=["booked", "available", "under_construction"])
    condition=StringField(required=True,choices=["clean","dirty","under_construction"])
    hotel_id=StringField(required=True)
    customer_name=StringField(required=False)
    customer_mobile=StringField(required=False)
    booked_from=StringField(required=False)
    booked_till=StringField(required=False)
    booking_price=StringField(required=False)
    booking_purpose=StringField(required=False)
    
    meta = {'collection': 'rooms'}

#Model for hotel
class Hotel(Document):
    hotel_name=StringField(required=True)
    district=StringField(required=True)
    state=StringField(required=True)
    landmark=StringField(required=True)
    
    meta = {'collection':'hotels'}
    
    
    