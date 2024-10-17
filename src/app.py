"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

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
    response_body = members
    
    return jsonify(response_body), 200

@app.route('/member/<int:id>', methods=['GET'])
def single_member(id):
    member = jackson_family.get_member(id)
    if not member:
        raise APIException('Member not found', status_code=400)
    
    response = {
        "first_name": member["first_name"],
        "id": member["id"],
        "age": member["age"],
        "lucky_numbers": member["lucky_numbers"]
    }
    
    return jsonify(response), 200


@app.route('/member',  methods=['POST'])
def create_member():
    data = request.json
    if not data:
        raise APIException('No data provided', status_code=400)
    if  'first_name' not in data or 'age' not  in data or 'lucky_numbers' not in data:
        raise APIException('Missing required data', status_code=400)
    
    #verificacion con metodo:
    result = jackson_family.add_member(data)
    if result == "invalid age":
        raise APIException('ivalid age', status_code=400)
    
    return ({"Message": "Miembro agregado"}),200


@app.route('/member/<int:id>', methods=['DELETE'])
def remove_member (id):
    member_off = jackson_family.delete_member(id)
    if not member_off:
        raise APIException('Member not deleted', status_code=400)
    return ({"done": True, "Message":"Miembro eliminado"}),200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
