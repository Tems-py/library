import bcrypt
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import engine
from models import User

login = Blueprint('login', __name__)

@login.route('/', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    print('Received data:', username , password)

    with Session(engine) as session:
        stmt = select(User).where(User.name.is_(username))
        user = session.scalars(stmt).one_or_none()

    # and bcrypt.check_password_hash(user.password, password)

    if user:
        access_token = create_access_token(identity=user.id)
        return jsonify({'message': 'Login Success', 'access_token': access_token})
    else:
        return jsonify({'message': 'Login Failed'}), 401

@login.route("/logut")
def logout():
    pass