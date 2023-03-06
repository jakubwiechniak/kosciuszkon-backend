import json
import math
import random
from datetime import timedelta

from app import app, db
from app.models import User, UserDailyMood, Messages, Questions, QuestionForConversation
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


@app.route('/match/<user_id>', methods=['GET'])
def match(user_id):
    if request.method == 'GET':
        users = [simple_user.to_dict() for simple_user in User.query.all()]
        current_user = User.query.get(user_id).to_dict()
        max = -1
        match_id = None
        match_tab = []
        for user in users:
            if int(user_id) != int(user['id']):
                score = 0

                # Zainteresowania
                current_interests = json.loads(current_user['user_interests'])
                user_interests = json.loads(user['user_interests'])
                for interest in current_interests:
                    for interest2 in user_interests:
                        if interest == interest2:
                            score += 15

                # Wiek
                points = 10 - math.fabs(current_user['age'] - user['age'])
                if points > 0:
                    score += points * 10

                # Samopoczucie
                date = datetime.today() - timedelta(days=3)
                current_moods = UserDailyMood.query.filter(and_(UserDailyMood.user_id == user_id,
                                                                UserDailyMood.timestamp > date)).all()
                user_moods = UserDailyMood.query.filter(and_(UserDailyMood.user_id == user['id'],
                                                             UserDailyMood.timestamp > date)).all()

                sum = 0
                for mood in current_moods:
                    sum += mood.mood

                sum2 = 0
                for mood in user_moods:
                    sum2 += mood.mood

                if current_moods == [] and user_moods == []:
                    score += math.fabs(sum/3 - sum2/3)

                # Typ osobowości 1
                if current_user['personality_type_one'] == user['personality_type_one']:
                    score += 50
                elif current_user['personality_type_one'] == 'Ciężko powiedzieć' or user['personality_type_one'] == 'Ciężko powiedzieć':
                    score += 25

                # Typ osobowości 1
                if current_user['personality_type_two'] == user['personality_type_two']:
                    score += 50
                elif current_user['personality_type_two'] == 'Ciężko powiedzieć' or user['personality_type_two'] == 'Ciężko powiedzieć':
                    score += 15

                if score > max:
                    max = score
                    match_id = user['id']
                if score > 100:
                    match_tab.append(user['id'])

        match_tab.append(match_id)
        print(match_tab)
        user = User.query.get(random.choice(match_tab)).to_dict()
        return user


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.json['email']).first()
        if user is None:
            user = User.query.filter_by(username=request.json['email']).first()
            if user is None:
                return failed("Nie istnieję użytkownik o podanej nazwie/e-mailu")
        if user.check_password(request.json['password']):
            return success(user.to_dict())
        else:
            return failed("Nieprawidłowe hasło")


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
            moods = UserDailyMood.query.filter_by(user_id=user_id).order_by(UserDailyMood.timestamp.desc())
            return success([simple_mood.to_dict() for simple_mood in moods])
        except:
            return failed("Pobranie listy codziennego samopoczucia użytkownika nie powiodło się")


@app.route('/user/<user_id>/friends', methods=['POST', 'DELETE'])
def add_friend(user_id):
    if request.method == 'POST':
        user = User.query.get(user_id)
        if user.add_friend(request.json['friend_id']):
            question = QuestionForConversation(user_one_id=user_id, user_two_id=request.json['friend_id'],
                                               question=random.choice([simple_question.to_dict() for simple_question in
                                                                       Questions.query.all()])['question'])
            db.session.add(question)
            db.session.commit()
            return success(user.friends)
        else:
            return failed("Użytkownik jest już przyjacielem")

    if request.method == 'DELETE':
        try:
            user = User.query.get(user_id)
            if user.remove_friend(request.json['friend_id']):
                db.session.commit()
                return success(user.friends)
            else:
                return failed("Przyjaciel nie istnieje")
        except:
            return failed("Usunięcie przyjaciela się nie udało")


@app.route('/friends/<user_id>', methods=['GET'])
def get_friends(user_id):
    if request.method == 'GET':
        user = User.query.get(user_id)
        friends = user.get_friends()
        print(friends)
        if friends:
            user_friends = []
            for friend_id in friends:
                f = User.query.get(friend_id)
                if f is not None:
                    user_friends.append(f.to_dict())
            return success(user_friends)
        else:
            return failed(None)


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
            print(QuestionForConversation.query.first().to_dict())
            for id in json.loads(user.friends):
                messages.append({
                    "id": id,
                    "messages": [message.to_dict() for message in Messages.query.filter(
                        or_(and_(Messages.receiver_id == user_id, Messages.sender_id == id),
                            and_(Messages.sender_id == user_id, Messages.receiver_id == id)))],
                    "question": [question.to_dict() for question in QuestionForConversation.query.filter(
                        or_(and_(QuestionForConversation.user_one_id == user_id,
                                 QuestionForConversation.user_two_id == id),
                            and_(QuestionForConversation.user_one_id == id,
                                 QuestionForConversation.user_two_id == user_id)))][0]['question'],
                })
            return success(messages)
        except:
            return failed("Nie udało pobrać się listy pytań")


@app.errorhandler(HTTPException)
def handle_exception(e):
    return failed("Podany URL nie istnieje")
