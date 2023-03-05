from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db
import uuid

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
    registration = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    pet_preference = db.Column(db.Integer, nullable=True)
    user_interests = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    mood = db.relationship('UserDailyMood', backref='user', lazy='dynamic')
    messages = db.relationship('Messages', backref='author', lazy='dynamic')
    match = db.relationship('Match', backref='chatter', lazy='dynamic')
    goals = db.relationship('Goals', backref='challenger', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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
            "registration": self.registration,
            "last_login": self.last_login,
            "pet_preference": self.pet_preference,
            "user_interests": self.user_interests,
            "description": self.description
        }
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "avatar": self.avatar,
            "dark_theme": self.dark_theme,
            "friends": self.friends,
            "registration": self.registration,
            "last_login": self.last_login,
            "pet_preference": self.pet_preference,
            "user_interests": self.user_interests,
            "description": self.description
        }
    
class Interests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    emoji = db.Column(db.String(30))

    def __repr__(self):
        return {"id": self.id, "name": self.name, "emoji": self.emoji}
    
    def to_dict(self):
        return {"id": self.id, "name": self.name, "emoji": self.emoji}
    
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
    reciever_id = db.Column(db.Integer)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text)
    type = db.Column(db.Integer)

    def __repr__(self):
        return {"id": self.id, "sender_id": self.sender_id, "reciever_id": self.reciever_id, "sent_at": self.sent_at, "content": self.content, "type": self.type}
    
    def to_dict(self):
        return {"id": self.id, "sender_id": self.sender_id, "reciever_id": self.reciever_id, "sent_at": self.sent_at, "content": self.content, "type": self.type}
    
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