"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import json
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite


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

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Fills DB with database.json test database. RUN THIS FIRST SO YOU CAN TEST
#  THE ROUTES! PD: RUN ONLY ONCE!!!
@app.route("/fill-db", methods=['GET'])
def fill_database():
    f = open("src/database.json", "r")
    content = f.read()
    jsondecoded = json.loads(content)

    for character in jsondecoded['characters']:
        new_character = Character(name = character['name'], height = character['height'],
        mass =character['mass'], hair_color = character['hair_color'], skin_color = character['skin_color'],
        eye_color = character['eye_color'], birth_year = character['birth_year'], gender = character['gender'],
        url = character['url'])
        db.session.add(new_character)


    for planet in jsondecoded['planets']:
        new_planet = Planet(name = planet['name'], diameter = planet['diameter'], rotation_period = planet['rotation_period'],
        orbital_period = planet['orbital_period'], gravity = planet['gravity'], population =planet['population'],
        climate = planet['climate'], terrain = planet['terrain'], surface_water = planet['surface_water'], url = planet['url'])
        db.session.add(new_planet)

    db.session.commit()

    return jsonify({"msg": "Database filled!"}), 200

# USER ROUTES
@app.route('/get-users', methods=['GET'])
def get_users():
    users = User.get_all_users()

    users = list(map(lambda user: user.name, users))

    response_body = {
        "msg": "Users list",
        "users": users
    }

    return jsonify(response_body), 200

@app.route('/get-user-by-id/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.get_user_by_id(user_id)

    response_body = {
        "msg": "User {name} found".format(name=user.name)
    }

    return jsonify(response_body), 200

@app.route('/add-user', methods=['POST'])
def add_user():
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')
    user = User(name=name, email=email, password=password)

    User.save(user)

    response_body = {
        "msg": "User added sussesfully",
        "user": user.name
    }

    return jsonify(response_body), 200

# CHARACTER ROUTES
@app.route('/get-characters', methods=['GET'])
def get_characters():
    characters = Character.get_all_characters()

    characters = list(map(lambda character: character.serialize(), characters))
    return jsonify(characters), 200

@app.route('/get-character/<int:character_id>', methods=['GET'])
def get_character_by_id(character_id):
    character = Character.get_character_by_id(character_id)

    response_body = {
        "msg": "Character found.",
        "character": character.serialize()
    }

    return jsonify(response_body), 200

@app.route('/add-character', methods=['POST'])
def add_character():
    name = request.json.get('name')
    height = request.json.get('height')
    mass = request.json.get('mass')
    hair_color = request.json.get('hair_color')
    skin_color = request.json.get('skin_color')
    eye_color = request.json.get('eye_color')
    birth_year = request.json.get('birth_year')
    gender = request.json.get('gender')
    url = request.json.get('url')
    character = Character(name=name, height=height, mass=mass, hair_color=hair_color,
    skin_color=skin_color, eye_color=eye_color, birth_year=birth_year, gender=gender,
    url=url)

    Character.save(character)

    response_body = {
        "msg": "Character added sussesfully",
        "character": character.name
    }

    return jsonify(response_body), 200

@app.route('/edit-character/<int:character_id>', methods=['PUT'])
def edit_character(character_id):
    character = Character.get_character_by_id(character_id)

    name = request.json.get('name')
    height = request.json.get('height')
    mass = request.json.get('mass')
    hair_color = request.json.get('hair_color')
    skin_color = request.json.get('skin_color')
    eye_color = request.json.get('eye_color')
    birth_year = request.json.get('birth_year')
    gender = request.json.get('gender')
    url = request.json.get('url')

    if name is None:
        return jsonify({"msg": "Name is mandatory"})

    character.name = name
    character.height = height
    character.mass = mass
    character.hair_color = hair_color
    character.skin_color = skin_color
    character.eye_color = eye_color
    character.birth_year = birth_year
    character.gender = gender
    character.url = url

    Character.commit()

    response_body = {
        "msg": "Character updated sussesfully",
        "character": character.name
    }

    return jsonify(response_body), 200

# PLANET ROUTES
@app.route('/get-planets', methods=['GET'])
def get_planets():
    planets = Planet.get_all_planets()

    planets = list(map(lambda planet: planet.serialize(), planets))
    return jsonify(planets), 200

@app.route('/get-planet/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):
    planet = Planet.get_planet_by_id(planet_id)
    
    response_body = {
        "msg": "Planet found.",
        "planet": planet.serialize()
    }

    return jsonify(response_body), 200

@app.route('/add-planet', methods=['POST'])
def add_planet():
    name = request.json.get('name')
    diameter = request.json.get('diameter')
    rotation_period = request.json.get('rotation_period')
    orbital_period = request.json.get('orbital_period')
    gravity = request.json.get('gravity')
    population = request.json.get('population')
    climate = request.json.get('climate')
    terrain = request.json.get('terrain')
    surface_water = request.json.get('surface_water')
    url = request.json.get('url')
    planet = Planet(name=name, diameter=diameter, rotation_period=rotation_period, orbital_period=orbital_period,
    gravity=gravity, population=population, climate=climate, terrain=terrain, surface_water=surface_water,
    url=url)

    Planet.save(planet)

    response_body = {
        "msg": "Planet added sussesfully",
        "planet": planet.name
    }

    return jsonify(response_body), 200

@app.route('/edit-planet/<int:planet_id>', methods=['PUT'])
def edit_planet(planet_id):
    planet = Planet.get_planet_by_id(planet_id)

    name = request.json.get('name')
    diameter = request.json.get('diameter')
    rotation_period = request.json.get('rotation_period')
    orbital_period = request.json.get('orbital_period')
    gravity = request.json.get('gravity')
    population = request.json.get('population')
    climate = request.json.get('climate')
    terrain = request.json.get('terrain')
    surface_water = request.json.get('surface_water')
    url = request.json.get('url')

    if name is None:
        return jsonify({"msg": "Name is mandatory"})

    planet.name = name
    planet.diameter = diameter
    planet.rotation_period = rotation_period
    planet.orbital_period = orbital_period
    planet.gravity = gravity
    planet.population = population
    planet.climate = climate
    planet.terrain = terrain
    planet.surface_water = surface_water
    planet.url = url

    Planet.commit()

    response_body = {
        "msg": "Planet updated sussesfully",
        "planet": planet.name
    }

    return jsonify(response_body), 200

# FAVORITES ROUTES
@app.route('/get-user-favorites/<int:user_id>', methods=['GET'])
def get_user_favorites(user_id):
    user = User.get_user_by_id(user_id)

    favorites = Favorite.query.filter_by(user_id = user.id)
    favorites = list(map(lambda favorite: favorite.serialize(), favorites))

    response_body = {
        "msg": "{name}'s favorites list".format(name=user.name),
        "favorites": favorites
    }

    return jsonify(response_body), 200

@app.route('/add-favorite/planet/<int:user_id>/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):
    user = User.get_user_by_id(user_id)
    planet = Planet.get_planet_by_id(planet_id)

    favorite_planet = Favorite(user_id=user.id, planet_id=planet.id)
   
    favorite_planet.save()

    favorites = Favorite.query.filter_by(user_id = user.id)
    favorites = list(map(lambda favorite: favorite.serialize(), favorites))

    response_body = {
        "msg": "planet {planet_name} has been added to {name} favorites list".format(name=user.name, planet_name=planet.name)
    }

    return jsonify(response_body), 200

@app.route('/add-favorite/character/<int:user_id>/<int:character_id>', methods=['POST'])
def add_favorite_character(user_id, character_id):
    user = User.get_user_by_id(user_id)
    character = Character.get_character_by_id(character_id)

    favorite_character = Favorite(user_id=user.id, character_id=character.id)
   
    favorite_character.save()

    favorites = Favorite.query.filter_by(user_id = user.id)
    favorites = list(map(lambda favorite: favorite.serialize(), favorites))

    response_body = {
        "msg": "character {character_name} has been added to {name} favorites list".format(name=user.name, character_name=character.name)
    }

    return jsonify(response_body), 200

@app.route('/delete-favorite/planet/<int:user_id>/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    user = User.get_user_by_id(user_id)
    planet = Planet.get_planet_by_id(planet_id)

    favorites = Favorite.query.filter_by(user_id = user.id)
    favorites = list(map(lambda favorite: favorite.serialize(), favorites))

    for favorite in favorites:
        for key in favorite.keys():
            if planet_id == favorite[key] and planet.id == planet_id:
                print('this is the planet_id to delete',favorite[key])
                favorites.remove(favorite)


    response_body = {
        "msg": "planet has been deleted from {name} favorites list".format(name=user.name)
    }

    return jsonify(response_body), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
