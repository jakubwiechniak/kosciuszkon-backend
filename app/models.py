from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    avatar = db.Column(db.Text)
    dark_theme = db.Column(db.Boolean)
    friends = db.Column(db.Text)
    registration = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    pet_preference = db.Column(db.Integer)
    user_interests = db.Column(db.Text)
    description = db.Column(db.Text)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        #return {c.name: getattr(self, c.name) for c in self.__table__.columns}
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