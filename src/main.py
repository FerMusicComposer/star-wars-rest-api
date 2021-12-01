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

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Fills DB with database.json test database. RUN THIS FIRST SO YOU CAN TEST THE ROUTES! 
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

    users = list(map(lambda user: user.serialize(), users))
    return jsonify(users), 200

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


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
