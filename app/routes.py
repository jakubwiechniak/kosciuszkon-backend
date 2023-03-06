import json

from app import app, db
from app.models import User, UserDailyMood, Messages
from app.common.response import success, failed
from app.common.interests import interests as proposed_interests
from app.common.personality_type_one import personality_type_one
from app.common.personality_type_two import personality_type_two
from flask import request
from werkzeug.exceptions import HTTPException
from deepface import DeepFace
from datetime import datetime
from sqlalchemy import or_, and_
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
    if request.method == 'PUT':
            print("body")
            print(request.json)
            User.query.filter_by(id=user_id).update(dict(request.json))

            db.session.commit()

            user = User.query.get(user_id)
            print(user.to_dict())
            return success(user.to_dict())
    if request.method == 'DELETE':
        try:
            user = User.query.get(user_id)
            db.session.delete(user)
            db.session.commit()

            return success({"id": user_id})
        except:
            return failed("Usuwanie użytkownika nie powiodło się")

@app.route('/token', methods=['POST'])
def check_token():
    if request.method == 'POST':
        try:
            user = User.query.filter_by(token=request.json['token']).first()
            if user is None:
                return failed("Token invalid")
            else:
                return success(user.to_dict())
        except:
            return failed("Coś poszło nie tak")
            

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


@app.route('/interests', methods=['GET'])
def interests():
    if request.method == 'GET':
        return success(proposed_interests)


@app.route('/personality-one', methods=['GET'])
def personality_one():
    if request.method == 'GET':
        return success(personality_type_one)


@app.route('/personality-two', methods=['GET'])
def personality_two():
    if request.method == 'GET':
        return success(personality_type_two)


@app.route('/mood', methods=['POST'])
def mood():
    if request.method == 'POST':
        try:
            f = open("image.jpg", "wb")
            
            f.write(base64.b64decode(request.json['image']))
            f.close()
            analyze = DeepFace.analyze(img_path="image.jpg")[0]['emotion']
            mood_value = 100 + round(analyze['happy']) - round(analyze['sad'])
            os.remove("image.jpg")

            user_daily_mood = UserDailyMood(user_id=request.json['user_id'], thankful_for=request.json['thankful_for'],
                                            mood=mood_value, timestamp=datetime.now())
            db.session.add(user_daily_mood)
            db.session.commit()
            return success(user_daily_mood.to_dict())
        except:
            return failed("Dodanie dzisiejszego samopoczucia nie powiodło się")


@app.route('/mood/<user_id>', methods=['GET'])
def mood_simple(user_id):
    if request.method == 'GET':
        try:
            moods = UserDailyMood.query.filter_by(user_id=user_id)
            return success([simple_mood.to_dict() for simple_mood in moods])
        except:
            return failed("Pobranie listy codziennego samopoczucia użytkownika nie powiodło się")

@app.route('/user/<user_id>/friends', methods=['POST', 'DELETE'])
def add_friend(user_id):
    if request.method == 'POST':
            user = User.query.get(user_id)
            if user.add_friend(request.json['friend_id']):
                db.session.commit()
                return success(user.friends)
            else:
                return failed("Friend already exists!")
        
    if request.method == 'DELETE':
        try:
            user = User.query.get(user_id)
            if user.remove_friend(request.json['friend_id']):
                db.session.commit()
                return success(user.friends)
            else:
                return failed("There's no such friend")
        except:
            return failed("Usunięcie przyjaciela się nie udało")
        
@app.route('/friends/<user_id>', methods=['GET'])
def get_friends(user_id):
    if request.method == 'GET':
        try:
            user = User.query.get(user_id)
            friends = user.get_friends()
            print(friends)
            if friends:
                return success([User.query.get(id).to_dict() for id in friends])
            else:
                return failed(None)
        except:
            return failed("Nie udało się pobrać listy przyjaciół")


@app.route('/message', methods=['POST'])
def message():
    if request.method == 'POST':
        try:
            message = Messages(sender_id=request.json['sender_id'], receiver_id=request.json['receiver_id'],
                               sent_at=datetime.now(), content=request.json['content'],
                               type=1)
            db.session.add(message)
            db.session.commit()
            return success(message.to_dict())
        except:
            return failed("Nie udało się wysłać wiadomości")


@app.route('/message/<user_id>', methods=['GET'])
def message_simple(user_id):
    if request.method == 'GET':
        try:
            user = User.query.get(user_id)
            messages = []
            for id in json.loads(user.friends):
                messages.append({
                    "id": id,
                    "messages": [message.to_dict() for message in Messages.query.filter(or_(and_(Messages.receiver_id == user_id, Messages.sender_id == id),
                                                                                            and_(Messages.sender_id == user_id, Messages.receiver_id == id)))]
                })
            return messages
        except:
            failed("Nie udało się pobrać listy wiadomości")


@app.errorhandler(HTTPException)
def handle_exception(e):
    return failed("Podany URL nie istnieje")
