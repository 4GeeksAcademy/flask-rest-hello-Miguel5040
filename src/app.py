"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from ast import excepthandler
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Planets, Vehicles, Favorites

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


# ----------------------------------------------------------------------------------------------------------------------------

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


# Obtener y crear usuarios
@app.route("/user", methods=["GET", "POST"])
def handle_user():
    if request.method == "POST":
        data = request.json  # Informacion recibida en el body de la peticion

        # Verificar los datos enviados en request
        if (data.get("name") is None or 
            data.get("lastName") is None or 
            data.get("email") is None):
            return jsonify({
                "message": "Falta informacion, verifica tu peticion."
            }), 400
        
        # Verificar que el email sea unico
        email_exist = User.query.filter_by(email=data["email"]).one_or_none()
        if email_exist:
            return jsonify({
                "message": "Email ya esta en uso"
            })
        
        # Crear el usuario
        new_user = User(name=data["name"], last_name=data["lastName"], email=data["email"])

        # Guardar en la base de datos
        try:
            db.session.add(new_user)
            db.session.commit()
        
        except Exception as error:
            db.session.rollback()
            print(error)
            return jsonify({
                "message": "Algo salio mal con la base de datos, intenta nuevamente"
            }), 500
        
        # Retornar repuesta positiva al usuario
        new_user_id = new_user.id
        return jsonify({
            "message": "Usuario creado con exito",
            "user_id": new_user_id
        }), 201
    
    if request.method == "GET":
        users = User.query.all()
        user_list = [{"id": user.id, "email": user.email} for user in users]
        return jsonify({'users': user_list})


# Solicitar personajes
@app.route("/characters", methods=["GET"])
def display_characters():
    characters = Characters.query.all()
    characters_list = [{"id": character.id, "name": character.name} for character in characters]
    return jsonify({'Characters': characters_list})


# Solicitar planetas
@app.route("/planets", methods=["GET"])
def display_planets():
    planets = Planets.query.all()
    planets_list = [{"id": planet.id, "name": planet.name} for planet in planets]
    return jsonify({'Planets': planets_list})    


# Solicitar vehiculos
@app.route("/vehicles", methods=["GET"])
def display_vehicles():
    vehicles = Vehicles.query.all()
    vehicles_list = [{"id": vechicle.id, "name": vechicle.name} for vechicle in vehicles]
    return jsonify({'Vehicles': vehicles_list})


# Solicitar personajes por el id
@app.route("/characters/<int:id>", methods=["GET"])
def display_character_info(id):
    character = Characters.query.get(id)
    
    if character is None:
        return jsonify({
            "message": "No existe un personaje con esa id"
        }), 404
    
    character_properties = [{"name": character.name, "birth_year": character.birth_year, "gender": character.gender, "height": character.height, "skin_color": character.skin_color, "eye_color": character.eye_color}]
    return jsonify({
        "message": "ok",
        "Properties": character_properties
    })


# Solicitar planetas por el id
@app.route("/planets/<int:id>", methods=["GET"])
def display_planet_info(id):
    planet = Planets.query.get(id)

    if planet is None:
        return jsonify({
            "message": "No existe un planeta con esa id"
        }), 404
    planet_properties = [{"name": planet.name, "diameter": planet.diameter, "gravity": planet.gravity, "population": planet.population, "climate": planet.climate, "terrain": planet.terrain}]
    return jsonify({
        "message": "ok",
        "properties": planet_properties
    })


# Solicitar vehiculos por el id
@app.route("/vehicles/<int:id>", methods=["GET"])
def display_vehicle_info(id):
    vehicle = Vehicles.query.get(id)

    if vehicle is None:
        return jsonify({
            "message": "No existe un vehiculo con esa id"
        }), 404
    
    vehicle_properties = [{"name": vehicle.name, "model": vehicle.model, "vehicle_class": vehicle.vehicle_class, "passengers": vehicle.passengers, "manufacturer": vehicle.manufacturer, "length": vehicle.length}]
    return jsonify({
        "message": "ok",
        "properties": vehicle_properties
    })


# Solicitar lista de favoritos con el id del usuario
@app.route("/user/<int:user_id>/favorites", methods=["GET"])
def display_favorites(user_id):
    user = User.query.get(user_id)

    if user is None:
        return jsonify({
            "message": "No existe un usuario con esa id"
        }), 404

    favorites_list = []
    for favorite in user.favorites:
        if favorite.characters:
            favorites_list.append({"id": favorite.characters.id, "name": favorite.characters.name})
        elif favorite.planets:
            favorites_list.append({"id": favorite.planets.id, "name": favorite.planets.name})
        elif favorite.vehicles:
            favorites_list.append({"id": favorite.vehicles.id, "name": favorite.vehicles.name})

    return jsonify({
        "favorites": favorites_list
    })   


# Agregar personaje favorito a usuario
@app.route("/user/<int:user_id>/favorite/character/<int:character_id>", methods=["POST"])
def add_favorite_character(user_id, character_id):

    # Verificar si el favorito ya existe para el usuario
    existing_favorite = Favorites.query.filter_by(
        user_id=user_id,
        id_characters=character_id
    ).first()

    if existing_favorite:
        return jsonify({
            "message": "Este personaje ya está en la lista de favoritos del usuario"
        }), 400

    # Creacion del favorito
    new_favorite_character = Favorites(user_id=user_id, id_characters=character_id)

    # Guardar en la base de datos
    try:
        db.session.add(new_favorite_character)
        db.session.commit()

    except Exception as error:
        db.session.rollback()
        print(error)
        return jsonify({
            "message": "Algo salio mal con la base de datos, intenta nuevamente"
        }), 500

    # Retornar repuesta positiva al usuario
    return jsonify({
        "message": "Agregado con exito"
    }), 201


# Agregar planeta favorito a usuario
@app.route("/user/<int:user_id>/favorite/planet/<int:planet_id>", methods=["POST"])
def add_favorite_planet(user_id, planet_id):

    # Verificar si el favorito ya existe para el usuario
    existing_favorite = Favorites.query.filter_by(
        user_id=user_id,
        id_planets=planet_id
    ).first()

    if existing_favorite:
        return jsonify({
            "message": "Este planeta ya está en la lista de favoritos del usuario"
        }), 400

    # Creacion del favorito
    new_favorite_planet = Favorites(user_id=user_id, id_planets=planet_id)

    # Guardar en la base de datos
    try:
        db.session.add(new_favorite_planet)
        db.session.commit()
        
    except Exception as error:
        db.session.rollback()
        print(error)
        return jsonify({
            "message": "Algo salio mal con la base de datos, intenta nuevamente"
        }), 500
        
    # Retornar repuesta positiva al usuario
    return jsonify({
        "message": "Agregado con exito"
    }), 201


# Agregar vehiculo favorito a usuario
@app.route("/user/<int:user_id>/favorite/vehicle/<int:vehicle_id>", methods=["POST"])
def add_favorite_vehicle(user_id, vehicle_id):

    # Verificar si el favorito ya existe para el usuario
    existing_favorite = Favorites.query.filter_by(
        user_id=user_id,
        id_vehicles=vehicle_id
    ).first()

    if existing_favorite:
        return jsonify({
            "message": "Este vehiculo ya está en la lista de favoritos del usuario"
        }), 400

    # Creacion del favorito
    new_favorite_vehicle = Favorites(user_id=user_id, id_vehicles=vehicle_id)

    # Guardar en la base de datos
    try:
        db.session.add(new_favorite_vehicle)
        db.session.commit()
        
    except Exception as error:
        db.session.rollback()
        print(error)
        return jsonify({
            "message": "Algo salio mal con la base de datos, intenta nuevamente"
        }), 500
        
    # Retornar repuesta positiva al usuario
    return jsonify({
        "message": "Agregado con exito"
    }), 201


# Eliminar personaje favorito de un usuario
@app.route("/user/<int:user_id>/favorite/character/<int:character_id>", methods=["DELETE"])
def delete_favorite_character(user_id, character_id):

    # Verificar si el usuario existe
    user = User.query.get(user_id)

    if user is None:
        return jsonify({
            "message": "No existe un usuario con esa id."
        }), 404

    # Extraer el favorito de la tabla favorites
    favorite_to_delete = Favorites.query.filter_by(id_characters=character_id, user_id=user_id).first()

    # Verificar si el favorito existe en los favoritos del Usuario
    if favorite_to_delete is None:
        return jsonify({
            "message": "No existe un favorito con esa id para el usuario."
        }), 404

    # Eliminar el favorito del usuario
    try:
        db.session.delete(favorite_to_delete)
        db.session.commit()

        return jsonify({
            "message": "Favorito eliminado con éxito."
        })

    except Exception as error:
        db.session.rollback()
        print(error)
        return jsonify({
            "message": "Algo salió mal al eliminar el favorito, intenta nuevamente."
        }), 500


# Eliminar planeta favorito de un usuario
@app.route("/user/<int:user_id>/favorite/planet/<int:planet_id>", methods=["DELETE"])
def delete_favorite_planet(user_id, planet_id):

    # Verificar si el usuario existe
    user = User.query.get(user_id)

    if user is None:
        return jsonify({
            "message": "No existe un usuario con esa id."
        }), 404

    # Extraer el favorito de la tabla favorites
    favorite_to_delete = Favorites.query.filter_by(id_planets=planet_id, user_id=user_id).first()

    # Verificar si el favorito existe en los favoritos del Usuario
    if favorite_to_delete is None:
        return jsonify({
            "message": "No existe un favorito con esa id para el usuario."
        }), 404

    # Eliminar el favorito del usuario
    try:
        db.session.delete(favorite_to_delete)
        db.session.commit()

        return jsonify({
            "message": "Favorito eliminado con éxito."
        })

    except Exception as error:
        db.session.rollback()
        print(error)
        return jsonify({
            "message": "Algo salió mal al eliminar el favorito, intenta nuevamente."
        }), 500


# Eliminar vehiculo favorito de un usuario
@app.route("/user/<int:user_id>/favorite/vehicle/<int:vehicle_id>", methods=["DELETE"])
def delete_favorite_vehicle(user_id, vehicle_id):

    # Verificar si el usuario existe
    user = User.query.get(user_id)

    if user is None:
        return jsonify({
            "message": "No existe un usuario con esa id."
        }), 404

    # Extraer el favorito de la tabla favorites
    favorite_to_delete = Favorites.query.filter_by(id_vehicles=vehicle_id, user_id=user_id).first()

    # Verificar si el favorito existe en los favoritos del Usuario
    if favorite_to_delete is None:
        return jsonify({
            "message": "No existe un favorito con esa id para el usuario."
        }), 404

    # Eliminar el favorito del usuario
    try:
        db.session.delete(favorite_to_delete)
        db.session.commit()

        return jsonify({
            "message": "Favorito eliminado con éxito."
        })

    except Exception as error:
        db.session.rollback()
        print(error)
        return jsonify({
            "message": "Algo salió mal al eliminar el favorito, intenta nuevamente."
        }), 500


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
