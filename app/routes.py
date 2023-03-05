from app import app, db
from app.models import User, Interests
from app.common.response import success, failed
from flask import request
from werkzeug.exceptions import HTTPException
from datetime import datetime
import base64, os


@app.route('/user', methods=['POST', 'GET'])
def user():
    if request.method == 'POST':
        user_props = {name: request.json[name] for name in request.json if name not in {'password'}}
        newuser = User(**user_props)
        newuser.set_password(request.json['password'])
        db.session.add(newuser)
        db.session.commit()
        return success(newuser.to_dict())

    elif request.method == 'GET':
        try:
            users = User.query.all()
            return success([simple_user.to_dict() for simple_user in users])
        except:
            return failed("Pobieranie listy użytkowników nie powiodło się")


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
                User.query.get(user).update({"last_login": datetime.utcnow})
                db.session.commit()
                post_update_user = User.query.get(user.id)
                return success(post_update_user.to_dict())
            else:
                return failed("Nieprawidłowe hasło")
        except:
            return failed("Logowanie nie powiodło się")


@app.route('/interests', methods=['POST'])
def interests():
    if request.method == 'POST':
        try:
            interest = Interests(name=request.json['name'], emoji=request.json['emoji'])
            db.session.add(interest)
            db.session.commit()

            return success(interest.to_dict())
        except:
            return failed("Wprowadzanie zainteresowania nie powiodło się")


@app.route('/interests/<interest_id>', methods=['GET', 'PUT', 'DELETE'])
def interests_simple(interest_id):
    if request.method == 'GET':
        try:
            interest = Interests.query.get(interest_id)
            return success(interest.to_dict())
        except:
            return failed("Nie znaleziono zainteresowania")

    if request.method == 'PUT':
        try:
            Interests.query.filter_by(id=interest_id).update(dict(request.json))
            db.session.commit()
            interest = Interests.query.get(interest_id)
            return success(interest.to_dict())
        except:
            return failed("Aktualizacja zainteresowania nie powiodła się")
    if request.method == 'DELETE':
        try:
            interest = Interests.query.get(interest_id)
            db.session.delete(interest)
            db.session.commit()
            return success({"id": interest_id})
        except:
            return failed("Usuwanie zainteresowania nie powiodło się")


@app.route('/mood', methods=['POST', 'GET'])
def mood():
    if request.method == 'POST':
        f = open("image.png", "wb")
        f.write(base64.b64decode(request.json['image']))
        f.close()
        face = DeepFace.analyze(img_path="image.png")
        os.remove("image.png")

        print(face[0]['dominant_emotion'])

        return face[0]['dominant_emotion']


@app.errorhandler(HTTPException)
def handle_exception(e):
    return failed("Podany URL nie istnieje")
