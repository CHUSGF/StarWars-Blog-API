"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Favorite, Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Mapa endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    users_serialized= list(map(lambda user: user.serialize(), users))
    return jsonify({"response": users_serialized})

# OBTENER TODOS LOS PERSONAJES
@app.route('/people', methods=['GET'])
def get_all_people():
    people = People.query.all()
    people_serialized= list(map(lambda people: people.serialize(), people))
    return jsonify({"response": people_serialized})

# OBTENER UN PERSONAJE
@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_people(people_id):
    people = People.get_by_id(people_id)
    if people:
        return jsonify({"response": people.serialize()})
    else:
        return jsonify({"error": "no encontrado"}), 401

# OBTENER PERSONAJES FAVORITOS
@app.route('/favorite/<int:user_id>/people/<int:people_id>', methods=['POST'])
def post_favorites_by_people(user_id, people_id):
    favorite = Favorite(user_id=user_id, people_id=people_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"favorites": favorite.serialize()})

# ELIMINAR UN PERSONAJE FAVORITO
@app.route('/favorite/<int:user_id>/people/<int:people_id>', methods=['DELETE'])
def delete_favorites_by_people(user_id, people_id):
    favorite = Favorite.query.filter_by(people_id=people_id).filter_by(user_id=user_id).first()
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"favorites": "Eliminado con exito"})

# OBTENER PERSONAJES FAVORITOS
@app.route('/users/<int:id>/favorites', methods=['GET'])
def get_favorites_by_user(id):
    favorites = Favorite.query.filter_by(user_id = id )
    return jsonify({"favorites": list(map(lambda favorite: favorite.serialize(), favorites))})


# OBTENER TODOS PLANETAS
@app.route('/planet', methods=['GET'])
def get_all_planet():
    planet = Planet.query.all()
    planet_serialized= list(map(lambda planet: planet.serialize(), planet))
    return jsonify({"response": planet_serialized})

# OBTENER UN PLANETA POR ID
@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    planet = Planet.get_by_id(planet_id)
    if planet:
        return jsonify({"response": planet.serialize()})
    else:
        return jsonify({"error": "no encontrado"}), 401

# OBTENER PLANETAS FAVORITOS
@app.route('/favorite/<int:user_id>/planet/<int:planet_id>', methods=['POST'])
def post_favorites_by_user(user_id, planet_id):
    favorite = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"favorites": favorite.serialize()})

# ELIMINAR UN PLANETA FAVORITO
@app.route('/favorite/<int:user_id>/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorites_by_user(user_id, planet_id):
    favorite = Favorite.query.filter_by(planet_id=planet_id).filter_by(user_id=user_id).first()
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"favorites": "Eliminado con exito"})


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
