from app import app, db
from app.models import User
from app.common.response import success, failed
from flask import request
from werkzeug.exceptions import HTTPException


@app.route('/index')
def index():
    return 'Hello World!'


@app.route('/user', methods=['POST', 'GET'])
def user():
    if request.method == 'POST':
        try:
            newuser = User(username=request.json['username'], email=request.json['email'],
                           first_name=request.json['first_name'], last_name=request.json['last_name'],
                           avatar=request.json['avatar'], dark_theme=request.json['dark_theme'],
                           friends=request.json['friends'], pet_preference=request.json['pet_preference'],
                           user_interests=request.json['user_interests'], description=request.json['description'])
            newuser.set_password(request.json['password'])
            db.session.add(newuser)
            db.session.commit()
            return success(newuser.to_dict())
        except:
            return failed("Rejestracja użytkownika nie powiodła się")
    elif request.method == 'GET':
        users = User.query.all()
        return success([simple_user.to_dict() for simple_user in users])
        # try:
        #     users = User.query.all()
        #     return success(users.to_dict())
        # except:
        #     return failed("Pobieranie listy użytkowników nie powiodło się")


@app.route('/user/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_simple(user_id):
    if request.method == 'GET':
        try:
            user = User.query.get(user_id)
            return success(user.to_dict())
        except:
            return failed("Nie znaleziono użytkownika")
    elif request.method == 'PUT':
        try:
            User.query.filter_by(id=user_id).update(dict(request.json))

            db.session.commit()

            user = User.query.get(user_id)

            return success(user.to_dict())
        except:
            return failed("Aktualizacja użytkownika nie powiodła się")
    elif request.method == 'DELETE':
        try:
            user = User.query.get(user_id)
            db.session.delete(user)
            db.session.commit()

            return success({"id": user_id})
        except:
            return failed("Usuwanie użytkownika nie powiodło się")


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        try:
            user = User.query.filter_by(email=request.json['email']).first()
            if user is None:
                user = User.query.filter_by(username=request.json['email']).first()
                if user is None:
                    return failed("Nie istnieję użytkownik o podanej nazwie/e-mailu")
            if user.check_password(request.json['password']):
                return success(user.to_dict())
            else:
                return failed("Nieprawidłowe hasło")
        except:
            return failed("Logowanie nie powiodło się")


@app.errorhandler(HTTPException)
def handle_exception(e):
    return failed("Podany URL nie istnieje")
