from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    preferences = relationship("Preference", back_populates="user")

class Preference(Base):
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content_type = Column(String(20))  # movie, book, music
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="preferences")
    recommendations = relationship("Recommendation", back_populates="preference")

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    preference_id = Column(Integer, ForeignKey("preferences.id"))
    title = Column(String(200))
    description = Column(Text)
    content_type = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    preference = relationship("Preference", back_populates="recommendations") 