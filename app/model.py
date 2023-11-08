from app import app, db_1
from sqlalchemy.sql import func
from dataclasses import dataclass
from datetime import datetime
from flask_login import UserMixin


@dataclass
class Compani(db_1.Model):
    id: int
    Campaning_Name: str
    Collection_Pointer: int
    Buffer_Pointer: int
    Status: str
    Attempts: int
    License_In_Use : int
    First_Call_Time: int
    Last_Call_Time: int
    Campaning_Data: int
    
    id = db_1.Column(db_1.Integer, primary_key=True)
    Campaning_Name = db_1.Column(db_1.String(200), unique=True, nullable=False)
    Collection_Pointer = db_1.Column(db_1.Integer)
    Buffer_Pointer = db_1.Column(db_1.Integer)
    Status = db_1.Column(db_1.String(100), nullable=False)
    Attempts = db_1.Column(db_1.Integer)
    License_In_Use = db_1.Column(db_1.Integer)
    First_Call_Time = db_1.Column(db_1.Integer)
    Last_Call_Time = db_1.Column(db_1.Integer)
    Campaning_Data = db_1.Column(db_1.DateTime(timezone=True),
                           server_default=func.now())

    def __repr__(self):
        return f'<Compani {self.Campaning_Name}>'
        

@app.login_manager.user_loader
def load_user(user_id):
    return db_1.session.query(User).get(user_id)

@dataclass
class User(db_1.Model, UserMixin):
    __tablename__ = 'user'
    id: int
    user_name: str
    password: str
    is_admin: bool
    created_on: str
    updated_on: str
    
    id = db_1.Column(db_1.Integer, primary_key=True)
    user_name = db_1.Column(db_1.String(100), nullable=False)
    password = db_1.Column(db_1.String(100), nullable=False)
    is_admin = db_1.Column(db_1.Boolean, default=False)
    created_on = db_1.Column(db_1.DateTime(), default=datetime.utcnow)
    updated_on = db_1.Column(db_1.DateTime(), default=datetime.utcnow,  onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.user_name}>'
    