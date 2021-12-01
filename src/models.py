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
    favorites = db.relationship('Favorite', lazy=True)
    

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email, 
            "favorites": self.favorites  
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
    favorites = db.relationship('Favorite', lazy=True)

    def __repr__(self):
        return '<Character %r>' % self.charactername

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
    favorites = db.relationship('Favorite', lazy=True)

    def __repr__(self):
        return '<Planet %r>' % self.planetname

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

class Favorite(db.Model, GeneralModel):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    character = db.relationship(Character)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet = db.relationship(Planet)

    def to_dict(self):
        return {}