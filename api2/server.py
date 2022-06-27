from flask import * 
from flasgger import Swagger

app = Flask(__name__) 
swagger = Swagger(app)

cars = [
    {
    "manufacturer" : "Porsche",
    "car_id" : "0",
    "model" : "911", 
    "price" : "135000",
    "colour" : "red",
    "owner" : "Lauren"
    },
    {
    "manufacturer" : "Nissan",
    "car_id" : "1",
    "model" : "GT-R", 
    "price" : "80000",
    "colour" : "green",
    "owner" : "Loren"
    },
    {
    "manufacturer" : "BMW",
    "car_id" : "2",
    "model" : "M3", 
    "price" : "60500",
    "colour" : "black",
    "owner" : "Xander"
    },
    {
    "manufacturer" : "Audi",
    "car_id" : "3",
    "model" : "S5", 
    "price" : "53000",
    "colour" : "blue",
    "owner" : "Alex"
    },
    {
    "manufacturer" : "Audi",
    "car_id" : "4",
    "model" : "TT", 
    "price" : "40000",
    "colour" : "black",
    "owner" : "Alexa"
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
            Welcome to the car club!
    """
    return "Welcome to the car club!"

@app.route("/cars", methods= ['GET'])
def get_car():
    """Endpoint to get all cars
    ---
    definitions:
      Message_to_get_cars:
        type: object
        properties:
          Cars:
            type: object
    responses:
      200:
        description: Returns a dictionary with all cars 
        schema:
          $ref: '#/definitions/Message_to_get_cars'
        examples:
          application/json: |
            {
              Cars: [
                      {
                        "manufacturer" : "Nissan", 
                        "car_id" : "1", 
                        "model" : "GT-R", 
                        "price" : "80000", 
                        "colour" : "black", 
                        "owner" : "Loren" 
                      }, 
                      {
                        "manufacturer" : "BMW", 
                        "car_id" : "2", 
                        "model" : "X3", 
                        "price" : "50000", 
                        "colour" : "black", 
                        "owner" : "Dan" 
                      }
                    ]
            }
    """
    return jsonify({'Cars' : cars})

@app.route("/cars/<string:id>", methods = ['GET'])
def get_car_by_id(id):
    """Endpoint to get a car by id
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
          Car:
            type: object
    responses:
      200:
        description: Returns a dictionary with the specific car 
        schema:
          $ref: '#/definitions/Message_to_get_by_id'
        examples:
          application/json: |
            {
              Car:  {
                      "manufacturer" : "Nissan", 
                      "car_id" : "1", 
                      "model" : "GT-R", 
                      "price" : "80000", 
                      "colour" : "black", 
                      "owner" : "Loren" 
                    }
            }
    """
    car = [car for car in cars if car['car_id'] == id]
    if len(car) == 0:
        return jsonify({'error': 'Not found'})
    return jsonify({"Car" : car[0]})

@app.route("/cars", methods = ['POST'])
def create():
    """Endpoint for creating a car
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
                      "manufacturer" : "Nissan", 
                      "car_id" : "1", 
                      "model" : "GT-R", 
                      "price" : "80000", 
                      "colour" : "black", 
                      "owner" : "Loren" 
                    }
            }
    """
    car = request.get_json()
    for item in cars:
        if(item['car_id'] == car['car_id']):
            return jsonify({'error': 'Please provide another car_id'})

    cars.append(car)

    return jsonify({"New" : car})

@app.route("/cars/<string:id>", methods = ['PUT'])
def update(id):
    """Endpoint for updating a car by id
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
                          "manufacturer" : "Nissan", 
                          "car_id" : 1, 
                          "model" : "GT-R", 
                          "price" : 80000, 
                          "colour" : "black", 
                          "owner" : "Loren" 
                        }
            }
    """
    car = [car for car in cars if car['car_id'] == id]
    if len(car) == 0:
        return jsonify({'error': 'Not found'})
    if 'manufacturer' in request.json and request.json['manufacturer'] != "":
        car[0]['manufacturer'] = request.json.get('manufacturer', car[0]['manufacturer'])
    if 'model' in request.json and request.json['model'] != "":
        car[0]['model'] = request.json.get('model', car[0]['model'])
    if 'price' in request.json and request.json['price'] != "":
        car[0]['price'] = request.json.get('price', car[0]['price'])
    if 'colour' in request.json and request.json['colour'] != "":
        car[0]['colour'] = request.json.get('colour', car[0]['colour'])
    if 'owner' in request.json and request.json['owner'] != "":
        car[0]['owner'] = request.json.get('owner', car[0]['owner'])
    
    return jsonify({'updated': car[0]})

@app.route("/cars/<string:id>", methods = ['DELETE'])
def delete(id):
    """Endpoint for deleting a car by id
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
    car = [car for car in cars if car['car_id'] == id]
    if len(car) == 0:
        return jsonify({'error': 'Not found'})
    cars.remove(car[0])
    return jsonify({'result' : True})






if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0')



