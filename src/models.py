import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    email = db.Column(String(250), unique=True, nullable=False)
    password = db.Column(String(250), nullable=False)
    first_name = db.Column(String(250), nullable=False)
    last_name = db.Column (String(250), nullable=False)
    favorites = db.relationship('Favorite', back_populates='user')

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "favorites": [favorite.serialize() for favorite in self.favorites] if self.favorites else [],
        }

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String(250), nullable=False)
    height = db.Column(String(10))
    weight = db.Column(String(10))
    gender = db.Column(String(10))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "weight": self.weight,
            "gender": self.gender,
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String(50), nullable=False)
    population = db.Column(Integer, nullable=False)
    diameter = db.Column(String(100), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "diameter": self.diameter,
        }

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(Integer, ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(Integer, ForeignKey('planet.id'), nullable=True)
    character_id = db.Column(Integer, ForeignKey('character.id'), nullable=True)
    user = db.relationship('User', back_populates='favorites')
    planet = db.relationship('Planet')
    character = db.relationship('Character')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "character_id": self.character_id,
        }