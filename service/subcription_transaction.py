import midtransclient
from models.users import Users
from config.database import connection
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import jwt_required, get_jwt_identity
import uuid

Session = sessionmaker(bind=connection)

def get_user_from_db(user_id):
    session = Session()
    try:
        user = session.query(Users).filter_by(id=user_id).first()
    finally:
        session.close()
    return user

def get_subcription_price(user_id):
    session = Session()
    try:
        subscription_price = session.query(Users).filter_by(id=user_id).first().subscription_price
    finally:
        session.close()
    return subscription_price

# Create Snap API instance
snap = midtransclient.Snap(
    is_production=False,
    client_key='SB-Mid-client-_yJX6mHyrKZMZ5cN', 
    server_key='SB-Mid-server-eZMbPuAmw3Clcc7YdO2s8SVu'
)

@jwt_required()
def create_transaction():
    user_id = get_jwt_identity()
    user = get_user_from_db(user_id)
    price = get_subcription_price(user_id)

    if user and price is not None:
        param = {
            "transaction_details": {
                "order_id": "ORDER-" + str(uuid.uuid4()),
                "gross_amount": price,
            },
            "customer_details": {
                "name": user.full_name,  
                "email": user.email,
            }
        }

        try:
            transaction = snap.create_transaction(param)
            transaction_token = transaction['token']
            return {"transaction_token": transaction_token}, 200
        except Exception as e:
            return {"error": str(e)}, 500
    else:
        return {"message": "User not found"}, 404