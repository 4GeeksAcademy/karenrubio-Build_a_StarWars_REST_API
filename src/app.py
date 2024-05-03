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
from models import db, User,People,Planet,FavoritePlanet,FavoritePeople,FavoriteStarship
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def get_people():
    all_people = People.query.all()
    results = list(map(lambda elemento: elemento.serialize() , all_people))

    return jsonify(results), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.filter_by(id=people_id).first()
    return jsonify(person.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets = Planet.query.all()
    results = list(map(lambda elemento: elemento.serialize() , all_planets))

    return jsonify(results), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.filter_by(id=planet_id).first()
    return jsonify(planet.serialize()), 200

@app.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    results = list(map(lambda elemento: elemento.serialize() , all_users))

    return jsonify(results), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return jsonify(user.serialize()), 200

# [GET] /users/favorites Listar todos los favoritos que pertenecen al usuario actual.
# [POST] /favorite/planet/<int:planet_id> Añade un nuevo planet favorito al usuario actual con el id = planet_id.
# [POST] /favorite/people/<int:people_id> Añade un nuevo people favorito al usuario actual con el id = people_id.
# [DELETE] /favorite/planet/<int:planet_id> Elimina un planet favorito con el id = planet_id.
# [DELETE] /favorite/people/<int:people_id> Elimina un people favorito con el id = people_id.
@app.route('/users/favorite_planet/<int:user_id>', methods=['GET'])
def user_favorite_planet(user_id):
    favorites = FavoritePlanet.query.filter_by(user_id=user_id).all()
    results = list(map(lambda favorite: favorite.serialize() , favorites))
    return jsonify(results), 200

@app.route('/users/favorite_people/<int:user_id>', methods=['GET'])
def user_favorite_people(user_id):
    favorites = FavoritePeople.query.filter_by(user_id=user_id).all()
    results = list(map(lambda favorite: favorite.serialize() , favorites))
    return jsonify(results), 200

@app.route('/users/favorite_starship/<int:user_id>', methods=['GET'])
def user_favorite_starship(user_id):
    favorites = FavoriteStarship.query.filter_by(user_id=user_id).all()
    results = list(map(lambda favorite: favorite.serialize() , favorites))
    return jsonify(results), 200

@app.route('/favorite/planet/<int:planet_id>/user/<int:user_id>', methods=['POST'])
def add_favorite_planet(planet_id, user_id):
    new_favorite = FavoritePlanet(planet_id = planet_id, user_id = user_id )
    db.session.add(new_favorite)
    db.session.commit()
    response_body = {
        "msg": "Favorito creado correctamente",
        "planet_id": planet_id,
        "user_id": user_id
    }
    return jsonify(response_body), 200

@app.route('/favorite/people/<int:people_id>/user/<int:user_id>', methods=['POST'])
def add_favorite_people(people_id, user_id):
    new_favorite = FavoritePeople(people_id = people_id, user_id = user_id )
    db.session.add(new_favorite)
    db.session.commit()
    response_body = {
        "msg": "Favorito creado correctamente",
        "people_id": people_id,
        "user_id": user_id
    }
    return jsonify(response_body), 200

@app.route('/favorite/starship/<int:starship_id>/user/<int:user_id>', methods=['POST'])
def add_favorite_starship(starship_id, user_id):
    new_favorite = FavoriteStarship(starship_id = starship_id, user_id = user_id )
    db.session.add(new_favorite)
    db.session.commit()
    response_body = {
        "msg": "Favorito creado correctamente",
        "starship_id": starship_id,
        "user_id": user_id
    }
    return jsonify(response_body), 200

@app.route('/favorite/planet/<int:planet_id>/user/<int:user_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id, user_id):
    favorite = FavoritePlanet.query.filter_by(planet_id = planet_id, user_id = user_id).first()
    db.session.delete(favorite)
    db.session.commit()
    response_body = {
        "msg": "Favorito eliminado correctamente",
        "planet_id": planet_id,
        "user_id": user_id
    }
    return jsonify(response_body), 200

@app.route('/favorite/people/<int:people_id>/user/<int:user_id>', methods=['DELETE'])
def delete_favorite_people(people_id, user_id):
    favorite = FavoritePeople.query.filter_by(people_id = people_id, user_id = user_id).first()
    db.session.delete(favorite)
    db.session.commit()
    response_body = {
        "msg": "Favorito eliminado correctamente",
        "people_id": people_id,
        "user_id": user_id
    }
    return jsonify(response_body), 200

@app.route('/favorite/starship/<int:starship_id>/user/<int:user_id>', methods=['DELETE'])
def delete_favorite_starship(starship_id, user_id):
    favorite = FavoriteStarship.query.filter_by(starship_id = starship_id, user_id = user_id).first()
    db.session.delete(favorite)
    db.session.commit()
    response_body = {
        "msg": "Favorito eliminado correctamente",
        "starship_id": starship_id,
        "user_id": user_id
    }
    return jsonify(response_body), 200
    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
