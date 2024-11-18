from flask import Flask, jsonify
from sqlalchemy import select
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from sqlalchemy.orm import Session

from database.database import engine
from database.models import User
from routes.login import login_bp

app = Flask(__name__)

app.config['SECRET_KEY'] = '123'
app.config["JWT_SECRET_KEY"] = '123'
app.config['JWT_TOKEN_LOCATION'] = ['headers']

app.register_blueprint(login_bp, url_prefix='/login')

jwt = JWTManager(app)

@app.route('/')
@jwt_required()
def hello_world():
    user_id = get_jwt_identity()
    with Session(engine) as session:
        stmt = select(User).where(User.id.is_(user_id))
        user = session.scalars(stmt).one_or_none()

    if user:
        return jsonify({'message': 'User found', 'name': user.id})
    else:
        return jsonify({'message': 'User not found'}), 404


if __name__ == '__main__':
    app.run()
