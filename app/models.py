from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import time
from app import db
import uuid
import json
import ast

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    token = db.Column(db.String(128), default=str(uuid.uuid4()))
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    age = db.Column(db.Integer)
    avatar = db.Column(db.Text, nullable=True)
    dark_theme = db.Column(db.Boolean, default=False)
    friends = db.Column(db.Text, nullable=True)
    pet_preference = db.Column(db.Integer, nullable=True)
    user_interests = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    personality_type_one = db.Column(db.Text, nullable=True)
    personality_type_two = db.Column(db.Text, nullable=True)
    mood = db.relationship('UserDailyMood', backref='user', lazy='dynamic')
    messages = db.relationship('Messages', backref='author', lazy='dynamic')
    match = db.relationship('Match', backref='chatter', lazy='dynamic')
    goals = db.relationship('Goals', backref='challenger', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def add_friend(self, friend_id):
        if self.friends is not None:
            friends_list = ast.literal_eval(self.friends)
            print(friends_list)
            if friend_id in friends_list:
                return False
            else:
                friends_list.append(friend_id)
                self.friends = str(friends_list)
                return friends_list
        else:
            self.friends = '[{}]'.format(friend_id)
            return self.friends
        
    def remove_friend(self, friend_id):
        if self.friends is not None:
            friends_list = ast.literal_eval(self.friends)
            if friend_id in friends_list:
                friends_list.remove(friend_id)
                self.friends = str(friends_list)
                return friends_list
            else:
                return False
        else:
            return False
        
    def get_friends(self):
        if self.friends is not None:
            friends_list = ast.literal_eval(self.friends)
            return friends_list
        else:
            return False

    def __repr__(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "avatar": self.avatar,
            "dark_theme": self.dark_theme,
            "friends": self.friends,
            "pet_preference": self.pet_preference,
            "user_interests": self.user_interests,
            "description": self.description,
            "personality_type_one": self.personality_type_one,
            "personality_type_two": self.personality_type_two,
        }

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "avatar": self.avatar,
            "age": self.age,
            "token": self.token,
            "dark_theme": self.dark_theme,
            "friends": self.friends,
            "pet_preference": self.pet_preference,
            "user_interests": self.user_interests,
            "description": self.description,
            "personality_type_one": self.personality_type_one,
            "personality_type_two": self.personality_type_two,
        }
    
class UserDailyMood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    mood = db.Column(db.Integer)
    thankful_for = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return {"id": self.id, "user_id": self.user_id, "mood": self.mood, "thankful_for": self.thankful_for, "timestamp": self.timestamp}
    
    def to_dict(self):
        return {"id": self.id, "user_id": self.user_id, "mood": self.mood, "thankful_for": self.thankful_for, "timestamp": self.timestamp}
    
class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer)
    sent_at = db.Column(db.TIMESTAMP, default=time.time())
    content = db.Column(db.Text)
    type = db.Column(db.Integer)

    def __repr__(self):
        return {"id": self.id, "sender_id": self.sender_id, "receiver_id": self.receiver_id, "sent_at": self.sent_at, "content": self.content, "type": self.type}
    
    def to_dict(self):
        return {"id": self.id, "sender_id": self.sender_id, "receiver_id": self.receiver_id, "sent_at": self.sent_at, "content": self.content, "type": self.type}
    
class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    second_user = db.Column(db.Integer)
    streak_days = db.Column(db.Integer)

    def __repr__(self):
        return {"id": self.id, "first_user": self.first_user, "second_user": self.second_user, "streak_days": self.streak_days}
    
    def to_dict(self):
        return {"id": self.id, "first_user": self.first_user, "second_user": self.second_user, "streak_days": self.streak_days}
    
class Goals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    emoji = db.Column(db.String(30))
    background = db.Column(db.String(7))
    days = db.Column(db.Integer)

    def __repr__(self):
        return {"id": self.id, "goal": self.goal, "user_id": self.user_id, "emoji": self.emoji, "background": self.background, "days": self.days}
    
    def to_dict(self):
        return {"id": self.id, "goal": self.goal, "user_id": self.user_id, "emoji": self.emoji, "background": self.background, "days": self.days}

class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    likes = db.Column(db.Integer)

    def __repr__(self):
        return {"id": self.id, "question": self.question, "likes": self.likes}
    
    def to_dict(self):
        return {"id": self.id, "question": self.question, "likes": self.likes}


class QuestionForConversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    user_one_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_two_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return {"id": self.id, "question": self.question, "user_one_id": self.user_one_id, "user_two_id": self.user_two_id }

    def to_dict(self):
        return {"id": self.id, "question": self.question, "user_one_id": self.user_one_id, "user_two_id": self.user_two_id }