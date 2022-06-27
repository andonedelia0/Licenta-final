from flask import * 
from flasgger import Swagger

app = Flask(__name__) 
swagger = Swagger(app)

pokemons = [
    {
    "name" :"piplup",
    "poke_id" : "0",
    "type" : "water", 
    "region" : "Sinnoh",
    "trainer" : "Dawn"
    },
    {
    "name" :"chimchar",
    "poke_id" : "1",
    "type" : "fire", 
    "region" : "Sinnoh",
    "trainer" : "Paul"
    },
    {
    "name" :"pikachu",
    "poke_id" : "2",
    "type" : "electric", 
    "region" : "Kanto",
    "trainer" : "Ash"
    },
    {
    "name" :"roselia",
    "poke_id" : "3",
    "type" : "grass", 
    "region" : "Hoen",
    "trainer" : "Drew"
    }
    ]

@app.route('/') 
def home():
    """Endpoint to greet the user
    ---
    definitions:
      Message_to_greet:
        type: string
    responses:
      200:
        description: Returns a welcome message
        schema:
          $ref: '#/definitions/Message_to_greet'
        examples:
          application/json: |
            Welcome to the pokemon club!
    """
    return "Welcome to the pokemon club!"

@app.route("/pokemons", methods= ['GET'])
def get_poke():
    """Endpoint to get all pokemons
    ---
    definitions:
      Message_to_get_pokemons:
        type: object
        properties:
          Pokemons:
            type: object
    responses:
      200:
        description: Returns a dictionary with all pokemons
        schema:
          $ref: '#/definitions/Message_to_get_pokemons'
        examples:
          application/json: |
            {
              Pokemons: [
                          {
                            "name": "aron", 
                            "poke_id": "1", 
                            "region": "Johto", 
                            "trainer": "Paul", 
                            "type": "steel"
                          }, 
                          {
                            "name": "piplup", 
                            "poke_id": "2", 
                            "region": "Sinnoh", 
                            "trainer": "Dawn", 
                            "type": "water"
                          }
                        ]
            }
    """
    return jsonify({'Pokemons' : pokemons})

@app.route("/pokemons/<string:id>", methods = ['GET'])
def get_poke_by_id(id):
    """Endpoint to get a pokemon by id
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
    definitions:
      Message_to_get_by_id:
        type: object
        properties:
          Pokemon:
            type: object
    responses:
      200:
        description: Returns a dictionary with the specific pokemon 
        schema:
          $ref: '#/definitions/Message_to_get_by_id'
        examples:
          application/json: |
            {
              Pokemon:  {
                          "name": "aron", 
                          "poke_id": "9", 
                          "region": "Johto", 
                          "trainer": "Paul", 
                          "type": "steel"
                        }
            }
    """
    pokemon = [pokemon for pokemon in pokemons if pokemon['poke_id'] == id]
    if len(pokemon) == 0:
        return jsonify({'error': 'Not found'})
    return jsonify({"Pokemon" : pokemon[0]})

@app.route("/pokemons", methods = ['POST'])
def create():
    """Endpoint for creating a pokemon
    ---
    definitions:
      Message_to_create:
        type: object
        properties:
          new:
            type: object
    responses:
      200:
        description: Returns a dictionary with the new object
        schema:
          $ref: '#/definitions/Message_to_create'
        examples:
          application/json: |
            {
              new:  {
                      "name": "aron", 
                      "poke_id": "9", 
                      "region": "Johto", 
                      "trainer": "Paul", 
                      "type": "steel"
                    }
            }
    """
    pokemon = request.get_json()
    for item in pokemons:
        if(item['poke_id'] == pokemon['poke_id']):
            return jsonify({'error': 'Please provide another poke_id'})

    pokemons.append(pokemon)

    return jsonify({"New" : pokemon})
   
@app.route("/pokemons/<string:id>", methods = ['PUT'])
def update(id):
    """Endpoint for updating a pokemon by id
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
    definitions:
      Message_to_update:
        type: object
        properties:
          updated:
            type: object
    responses:
      200:
        description: Returns a dictionary with the updated object
        schema:
          $ref: '#/definitions/Message_to_update'
        examples:
          application/json: |
            {
              updated:  {
                          "name": "aron", 
                          "poke_id": "0", 
                          "region": "Johto", 
                          "trainer": "Paul", 
                          "type": "steel"
                        }
            }
    """
    pokemon = [pokemon for pokemon in pokemons if pokemon['poke_id'] == id]
    if len(pokemon) == 0:
        return jsonify({'error': 'Not found'})
    if 'name' in request.json and request.json['name'] != "":
        pokemon[0]['name'] = request.json.get('name', pokemon[0]['name'])
    if 'region' in request.json and request.json['region'] != "":
        pokemon[0]['region'] = request.json.get('region', pokemon[0]['region'])
    if 'trainer' in request.json and request.json['trainer'] != "":
        pokemon[0]['trainer'] = request.json.get('trainer', pokemon[0]['trainer'])
    if 'type' in request.json and request.json['type'] != "":
        pokemon[0]['type'] = request.json.get('type', pokemon[0]['type'])
   
    return jsonify({'updated': pokemon[0]})

@app.route("/pokemons/<string:id>", methods = ['DELETE'])
def delete(id):
    """Endpoint for deleting a pokemon by id
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
    definitions:
      Message_to_delete:
        type: object
        properties:
          result:
            type: boolean
    responses:
      200:
        description: A message to validate the result of the delete operation
        schema:
          $ref: '#/definitions/Message_to_delete'
        examples:
          application/json: |
            {"result": True}
    """
    pokemon = [pokemon for pokemon in pokemons if pokemon['poke_id'] == id]
    if len(pokemon) == 0:
        return jsonify({'error': 'Not found'})
    pokemons.remove(pokemon[0])
    return jsonify({'result' : True})





if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0')



