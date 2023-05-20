"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }

    return jsonify(response_body), 200

@app.route('/members', methods=['POST'])
def add_member():
    # Obtén los datos enviados en el cuerpo de la solicitud
    data = request.get_json()

    # Valida que los datos requeridos estén presentes
    required_fields = ['first_name', 'last_name', 'age', 'lucky_numbers']
    for field in required_fields:
        if field not in data:
            raise APIException(f"Missing required field: {field}", status_code=400)

    # Crea un nuevo miembro basado en los datos recibidos
    new_member = {
        "id": len(jackson_family.get_all_members()) + 1,
        "first_name": data['first_name'],
        "last_name": data['last_name'],
        "age": data['age'],
        "lucky_numbers": data['lucky_numbers']
    }

    # Agrega el nuevo miembro a la estructura de datos de la familia Jackson
    jackson_family.add_member(new_member)

    # Devuelve una respuesta con el nuevo miembro agregado
    return jsonify(new_member), 201

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
    personas = [
        {
            "id": 1,
            "first_name": "John",
            "last_name": "Jackson",
            "age": 33,
            "lucky_numbers": [7, 13, 22]
        },
        {
            "id": 2,
            "first_name": "Jane",
            "last_name": "Jackson",
            "age": 35,
            "lucky_numbers": [10, 14, 3]
        },
        {
            "id": 3,
            "first_name": "Jimmy",
            "last_name": "Jackson",
            "age": 5,
            "lucky_numbers": [1]
        }
    ]

    for p in personas:
        jackson_family.add_member(p)

    
    
