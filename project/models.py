from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    house_area = Column(Float, nullable=False)

    usage_logs = relationship("UsageLog", back_populates="user")
    security_events = relationship("SecurityEvent", back_populates="user")
    feedbacks = relationship("Feedback", back_populates="user")


class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)

    usage_logs = relationship("UsageLog", back_populates="device")


class UsageLog(Base):
    __tablename__ = "usage_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    device_id = Column(Integer, ForeignKey("devices.id"))
    start_time = Column(DateTime, default=datetime.utcnow)
    finish_time = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="usage_logs")
    device = relationship("Device", back_populates="usage_logs")


class SecurityEvent(Base):
    __tablename__ = "security_events"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event = Column(String)
    severity = Column(String, default="info")  # 可为 info, warning, critical
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="security_events")


class Feedback(Base):
    __tablename__ = "feedbacks"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="feedbacks")
