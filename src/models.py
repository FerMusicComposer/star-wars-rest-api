from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class GeneralModel: 
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def commit ():
        db.session.commit()

    def add (self):
        db.session.add(self)
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class User(db.Model, GeneralModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    favorite_planets = db.relationship('Favorite_Planet', backref='user', lazy=True)
    favorite_characters = db.relationship('Favorite_Character', backref='user', lazy=True)
    

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email, 
            "favorite_planets": self.favorite_planets  
        }

    def get_user_by_id(id):
        return User.query.filter_by(id=id).first()

    def get_all_users():
        return User.query.all()

class Character(db.Model, GeneralModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)    
    height = db.Column(db.Integer)
    mass = db.Column(db.Integer)
    hair_color = db.Column(db.String(250))
    skin_color = db.Column(db.String(250))
    eye_color = db.Column(db.String(250))
    birth_year = db.Column(db.String(250))
    gender = db.Column(db.String(250))
    url = db.Column(db.String(250))
    favorite_characters = db.relationship('Favorite_Character', backref='character', lazy=True)

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,   
            "mass": self.mass,   
            "hair_color": self.hair_color,   
            "skin_color": self.skin_color,   
            "eye_color": self.eye_color,   
            "birth_year": self.birth_year,   
            "gender": self.gender,   
            "url": self.url,   
        }
    def get_character_by_id(id):
        return Character.query.filter_by(id=id).first()

    def get_all_characters():
        return Character.query.all()

class Planet(db.Model, GeneralModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)  
    diameter = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    gravity = db.Column(db.String(250))
    population = db.Column(db.Integer)
    climate = db.Column(db.String(250))
    terrain = db.Column(db.String(250))
    surface_water = db.Column(db.Integer)
    url = db.Column(db.String(250))
    favorite_planet = db.relationship('Favorite_Planet', backref='planet', lazy=True)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,   
            "rotation_period": self.rotation_period,   
            "orbital_period": self.orbital_period,   
            "gravity": self.gravity,   
            "population": self.population,   
            "climate": self.climate,   
            "terrain": self.terrain,   
            "surface_water": self.surface_water,   
            "url": self.url,   
        }

    def get_planet_by_id(id):
        return Planet.query.filter_by(id=id).first()

    def get_all_planets():
        return Planet.query.all()

class Favorite_Planet(db.Model, GeneralModel):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), primary_key=True)

    def serialize(self):
        return {
            "user_id": self.user_id,
            "planet_id": self.planet_id,
        }

class Favorite_Character(db.Model, GeneralModel):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), primary_key=True)

    def serialize(self):
        return {
            "user_id": self.user_id,
            "character_id": self.character_id,
        }
