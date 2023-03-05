from app import app, db
from app.models import User
from flask import request

@app.route('/')
@app.route('/index')
def index():
    return 'Hello World!'

@app.route('/user', methods=['POST'])
def register():
    newuser = User(username=request.json['username'], email=request.json['email'], first_name=request.json['first_name'], last_name=request.json['last_name'], avatar=request.json['avatar'], dark_theme=request.json['dark_theme'], friends=request.json['friends'], pet_preference=request.json['pet_preference'], user_interests=request.json['user_interests'], description=request.json['description'])
    newuser.set_password(request.json['password'])
    db.session.add(newuser)
    db.session.commit()
    return newuser.to_dict()

@app.route('/user/<user_id>', methods = ['GET', 'PUT', 'DELETE'])
def user(user_id):
    if request.method == 'GET':
        user = User.query.get(user_id)
        return user


@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.json['email']).first()
        if user.check_password(request.json['password']):
            return {"success": True}
        else:
            return {"success": False}