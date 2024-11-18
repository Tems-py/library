from flask import Flask, jsonify
from sqlalchemy import create_engine, select
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.orm import Session

from models import Base, User
from routes.login import login

app = Flask(__name__)

app.config['SECRET_KEY'] = 'duduududuauewu12332132131duahduawhudwahuidhawuidhauiwbnduiawbnduwanbdawnjdawnjdawnujdan2'
app.config["JWT_SECRET_KEY"] = '73127838128y31y331231231228y123'
app.config['JWT_TOKEN_LOCATION'] = ['headers']

app.register_blueprint(login, url_prefix='/login')

jwt = JWTManager(app)

engine = create_engine("sqlite:///database.db", echo=True)
Base.metadata.create_all(bind=engine)

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
