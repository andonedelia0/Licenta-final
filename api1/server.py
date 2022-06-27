from flask import * 
from flasgger import Swagger

app = Flask(__name__) 
swagger = Swagger(app)

books = [
    {
    "title": "Two Years' Vacation", 
    "book_id": "0", 
    "author": "Jules Verne", 
    "year_written": "1888", 
    "edition": "Pierre-Jules Hetzel", 
    "price":  "30.7"
    },
    {
    "title": "Anna Karenina", 
    "book_id": "1",
    "author": "Leo Tolstoy", 
    "year_written": "1878", 
    "edition": "The Russian Messenger", 
    "price":  "25.5"
    },
    {
    "title": "Tom Sawyer", 
    "book_id": "2",
    "author": "Mark Twain", 
    "year_written": "1876", 
    "edition": "American Publishing Company", 
    "price":  "37.75"
    },
    {
    "title": "Harry Potter", 
    "book_id": "3",
    "author": "J.K. Rowling", 
    "year_written": "2000", 
    "edition": "Harcourt Brace", 
    "price":  "19.95"
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
            Welcome to the book club!
    """
    return "Welcome to the book club!"

@app.route("/books", methods= ['GET'])
def get_book():
    """Endpoint to get all books
    ---
    definitions:
      Message_to_get_books:
        type: object
        properties:
          Books:
            type: object
    responses:
      200:
        description: Returns a dictionary with all books
        schema:
          $ref: '#/definitions/Message_to_get_books'
        examples:
          application/json: |
            {
              Books:  [
                        {
                          "title": "Hamlet, Prince of Denmark", 
                          "book_id": 7, 
                          "author": "Shakespeare", 
                          "year_written": 1603, 
                          "edition": "Signet  Classics", 
                          "price":  7.95
                        }, 
                        {
                          "author": "Tolstoy, Leo", 
                          "book_id": 0, 
                          "edition": "Penguin", 
                          "price": 12.7, 
                          "title": "War and Peace", 
                          "year_written": 1865
                        }
                      ]
            }
    """
    return jsonify({'Books' : books})

@app.route("/books/<string:id>", methods = ['GET'])
def get_book_by_id(id):
    """Endpoint to get a book by id
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
          Book:
            type: object
    responses:
      200:
        description: Returns a dictionary with the specific book 
        schema:
          $ref: '#/definitions/Message_to_get_by_id'
        examples:
          application/json: |
            {
              Book: {
                      "title": "Hamlet, Prince of Denmark", 
                      "book_id": "7", 
                      "author": "Shakespeare", 
                      "year_written": 1603, 
                      "edition": "Signet  Classics", 
                      "price":  "7.95"
                    }
            }
    """
    book = [book for book in books if book['book_id'] == id]
    if len(book) == 0:
        return jsonify({'error': 'Not found'})
    return jsonify({"Book" : book[0]})

@app.route("/books", methods = ['POST'])
def create():
    """Endpoint for creating a book
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
                      "title": "Hamlet, Prince of Denmark", 
                      "book_id": "7", 
                      "author": "Shakespeare", 
                      "year_written": 1603, 
                      "edition": "Signet  Classics", 
                      "price":  "7.95"
                    }
            }
    """
    book = request.get_json()
    for item in books:
        if(item['book_id'] == book['book_id']):
            return jsonify({'error': 'Please provide another book_id'})

    books.append(book)

    return jsonify({"New" : book})
    
@app.route("/books/<string:id>", methods = ['PUT'])
def update(id):
    """Endpoint for updating a book by id
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
                          "title": "Hamlet, Prince of Denmark", 
                          "book_id": "7", 
                          "author": "Shakespeare", 
                          "year_written": 1603, 
                          "edition": "Signet  Classics", 
                          "price":  "7.95"
                        }
            }
    """
    book = [book for book in books if book['book_id'] == id]
    if len(book) == 0:
        return jsonify({'error': 'Not found'})
    if 'title' in request.json and request.json['title'] != "":
        book[0]['title'] = request.json.get('title', book[0]['title'])
    if 'author' in request.json and request.json['author'] != "":
        book[0]['author'] = request.json.get('author', book[0]['author'])
    if 'year_written' in request.json and request.json['year_written'] != "":
        book[0]['year_written'] = request.json.get('year_written', book[0]['year_written'])
    if 'edition' in request.json and request.json['edition'] != "":
        book[0]['edition'] = request.json.get('edition', book[0]['edition'])
    if 'price' in request.json and request.json['price'] != "":
        book[0]['price'] = request.json.get('price', book[0]['price'])
    
    return jsonify({'updated': book[0]})

@app.route("/books/<string:id>", methods = ['DELETE'])
def delete(id):
    """Endpoint for deleting a book by id
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
    book = [book for book in books if book['book_id'] == id]
    if len(book) == 0:
        return jsonify({'error': 'Not found'})
    books.remove(book[0])
    return jsonify({'result' : True})






if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0')



