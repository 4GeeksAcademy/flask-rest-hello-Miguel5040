from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):  # Parent
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    favorites = db.relationship("Favorites", back_populates="user")

    def __repr__(self):
        return '<User %r>' % self.name


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email
        }


class Favorites(db.Model):  # Child
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", back_populates="favorites")

    id_characters = db.Column(db.Integer, db.ForeignKey("characters.id"))
    characters = db.relationship("Characters", back_populates="favorites")

    id_planets = db.Column(db.Integer, db.ForeignKey("planets.id"))
    planets = db.relationship("Planets", back_populates="favorites")

    id_vehicles = db.Column(db.Integer, db.ForeignKey("vehicles.id"))
    vehicles = db.relationship("Vehicles", back_populates="favorites")

 
class Characters(db.Model):  # Parent
    id = db.Column(db.Integer, primary_key=True)
    favorites = db.relationship("Favorites", back_populates="characters")

    name = db.Column(db.String(200))
    birth_year = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    height = db.Column(db.Integer)
    skin_color = db.Column(db.String(100))
    eye_color = db.Column(db.String(100))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "height": self.height,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color
        }


class Planets(db.Model):  # Parent
    id = db.Column(db.Integer, primary_key=True)
    favorites = db.relationship("Favorites", back_populates="planets")

    name = db.Column(db.String(200))
    diameter = db.Column(db.Integer)
    gravity = db.Column(db.String(100))
    population = db.Column(db.Integer)
    climate = db.Column(db.String(100))
    terrain = db.Column(db.String(100))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain
        }


class Vehicles(db.Model):  # Parent
    id = db.Column(db.Integer, primary_key=True)
    favorites = db.relationship("Favorites", back_populates="vehicles")

    name = db.Column(db.String(200))
    model = db.Column(db.String(100))
    vehicle_class = db.Column(db.String(100))
    passengers = db.Column(db.Integer)
    manufacturer = db.Column(db.String(100))
    length = db.Column(db.Integer)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "passengers": self.passengers,
            "manufacturer": self.manufacturer,
            "length": self.length
        }