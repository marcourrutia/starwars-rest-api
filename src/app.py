from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Character, Planet, Favorite
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///startwars-rest.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
Migrate(app, db)

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
db.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/character', methods=['GET'])
def get_characters():
    characters = session.query(Character).all()
    return jsonify([char.serialize() for char in characters]), 200

@app.route('/character/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = session.query(Character).get(character_id)
    if character:
        return jsonify(character.serialize()), 200
    return jsonify({"error": "Character not found"}), 404

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = session.query(Planet).all()
    return jsonify([planet.serialize() for planet in planets]), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = session.query(Planet).get(planet_id)
    if planet:
        return jsonify(planet.serialize()), 200
    return jsonify({"error": "Planet not found"}), 404

@app.route('/users', methods=['GET'])
def get_users():
    users = session.query(User).all()
    return jsonify([user.serialize() for user in users]), 200

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = session.query(User).get(user_id)
    if user:
        return jsonify([fav.serialize() for fav in user.favorites]), 200
    return jsonify({"error": "User not found"}), 404

@app.route('/favorite/planet/<int:user_id>/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):
    favorite = Favorite(user_id=user_id, planet_id=planet_id)
    try:
        session.add(favorite)
        session.commit()
        return jsonify({"message": "Planet added to favorites"}), 201
    except IntegrityError:
        session.rollback()
        return jsonify({"error": "Planet is already in favorites"}), 400

@app.route('/favorite/character/<int:user_id>/<int:character_id>', methods=['POST'])
def add_favorite_character(user_id, character_id):
    favorite = Favorite(user_id=user_id, character_id=character_id)
    try:
        session.add(favorite)
        session.commit()
        return jsonify({"message": "Character added to favorites"}), 201
    except IntegrityError:
        session.rollback()
        return jsonify({"error": "Character is already in favorites"}), 400

@app.route('/favorite/planet/<int:user_id>/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    favorite = session.query(Favorite).filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite:
        session.delete(favorite)
        session.commit()
        return jsonify({"message": "Favorite planet removed"}), 200
    return jsonify({"error": "Favorite planet not found"}), 404

@app.route('/favorite/character/<int:user_id>/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(user_id, character_id):
    favorite = session.query(Favorite).filter_by(user_id=user_id, character_id=character_id).first()
    if favorite:
        session.delete(favorite)
        session.commit()
        return jsonify({"message": "Favorite character removed"}), 200
    return jsonify({"error": "Favorite character not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)