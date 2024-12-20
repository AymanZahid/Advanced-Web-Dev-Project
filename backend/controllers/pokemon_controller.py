from flask import Blueprint, abort, request, jsonify
from services.account_service import get_account_name
from services.jwt_token_service import token_required
from services.pokemon_service import remove_move, add_moves, delete_pokemon, update_pokemon, is_created_by_user, get_pokemon_by_id, get_all_pokemons, add_pokemon, validate_data

pokemon_bp = Blueprint("pokemon_bp", __name__)

# Get all pokemon in the database
@pokemon_bp.route("/pokemon", methods=["GET"])
def manage_pokemon():
    # Get all Pokemon data based of given name and creator filters
    if request.method == "GET":
        name = "" if not request.args.get("name") else request.args.get("name")
        creator = "" if not request.args.get("creator") else request.args.get("creator")
        
        pokemon_data = get_all_pokemons(name, creator, False)
        
        return jsonify(pokemon_data)
    

@pokemon_bp.route("/pokemon/<int:pokemon_id>", methods=["GET"])
def manage_by_id_pokemon(pokemon_id):
    # Get Pokemon data based on id
    if request.method == "GET":
        pokemon_data = get_pokemon_by_id(pokemon_id)
        return  jsonify(pokemon_data)
    
# Update and Delete Pokemon
@pokemon_bp.route("/user/pokemon/<int:pokemon_id>", methods=["PUT", "DELETE"])
@token_required
def modify_delete_pokemon(user_data, pokemon_id):
    # Update Pokemon data based on id
    if request.method == "PUT":
        if not is_created_by_user(pokemon_id, user_data.username):
            abort(401, "You cannot edit a pokemon you didn't create")

        data = request.json
        types, name, image, hp, attack, defense, sp_attack, sp_defense, speed = validate_data(data)

        update_pokemon(types, name, image, pokemon_id, hp, attack, defense, sp_attack, sp_defense, speed )

        return jsonify({"message": "pokemon successfully updated!"})
    
    # Delete pokemon data based on id
    if request.method == "DELETE":
        delete_pokemon(pokemon_id)
        return jsonify({"message": "pokemon successfully deleted!"})


@pokemon_bp.route("/user/pokemon", methods=["POST", "GET"])
@token_required
def manage_user_pokemon(user_data):
    # Create a pokemon 
    if request.method == "POST":
        data = request.json
        types, name, image, hp, attack, defense, sp_attack, sp_defense, speed = validate_data(data)

        # Check if types are valid
        id = add_pokemon(types, name, image, user_data.username, hp, attack, defense, sp_attack, sp_defense, speed)

        return jsonify({"message": "pokemon successfully added!", "id": id})
    
    # Get all pokemon based of the logged in accounts username
    if request.method == "GET":
        print(user_data.username)
        pokemon_data = get_all_pokemons("", user_data.username, True)

        return jsonify(pokemon_data)
    
# Get pokemon from other users
@pokemon_bp.route("/user/pokemon/<string:username>", methods=["GET"])
def manage_other_user_pokemon(username):
    # Get all pokemon based of an accounts username
    if request.method == "GET":
        pokemon_data = get_all_pokemons("", username, True)
        return jsonify(pokemon_data)

# Add a new move to pokemon
@pokemon_bp.route("/user/pokemon/<string:pokemon_id>/move", methods=["POST", "DELETE"])
@token_required
def manage_pokemon_moves(user_data, pokemon_id):
    # Add a move to a pokemon    
    if request.method == "POST":
        data = request.json
        add_moves(data, pokemon_id)

        return jsonify({"message": "move successfully added to pokemon"})
    # Delete a move from a pokemon
    if request.method == "DELETE":
        data = request.json
        remove_move(data, pokemon_id)

        return jsonify({"message": "move successfully removed"})
