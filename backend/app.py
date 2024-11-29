import sys

from flask import Flask
from flask_cors import CORS

from extensions import db, migrate
from config import Config

from controllers.account_controller import account_bp
from controllers.types_controller import type_bp
from controllers.pokemon_controller import pokemon_bp
from controllers.move_controller import move_bp
from controllers.pokeapi_controller import pokeapi_bp

sys.dont_write_bytecode = True

def create_app():
    """
    Create and configure Flask App.

    Initializes the database, controllers and the blueprints 
    for each of the controllers. Returning the Flask Application

    """

    app = Flask(__name__)

    # Enables CORS
    CORS(app, supports_credentials=True)
    
    app.config.from_object(Config) 

    # Sets SQLAlchemy database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    
    # Intializes the database 
    db.init_app(app)
    migrate.init_app(app, db)

    # Registers blueprints for the controllers.
    app.register_blueprint(account_bp)
    app.register_blueprint(type_bp)
    app.register_blueprint(pokemon_bp)
    app.register_blueprint(move_bp)
    app.register_blueprint(pokeapi_bp)

    return app

# Creates the app
app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
