from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class DeviceStatus(Base):
    __tablename__ = 'device_status'
    
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(15), nullable=False)
    devices = db.relationship('Device', backref='status')

class DeviceLocation(Base):
    __tablename__ = 'device_location'
    
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    device = db.relationship('Device', backref='location', uselist=False)

class Device(Base):
    __tablename__ = 'device'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    battery = db.Column(db.Float(precision=2))
    status_id = db.Column(db.Integer, db.ForeignKey("device_status.id"))
    location_id = db.Column(db.Integer, db.ForeignKey("device_location.id"))
