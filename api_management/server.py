from operator import truth
from flask import *
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import requests
import time
import os 
app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'users'
app.config["MONGO_URI"] =  "mongodb://mongodb:27017/users"

mongo = PyMongo(app)


#USERS
#get all users
@app.route('/users', methods = ['GET'])
def get_users():
    users = mongo.db.users      #the collection i have in my db
    output = []

    for query in users.find():        #find all the documents in the collection    
        output.append({'_id': str(query['_id']), 'name': query['name'], 'password': query['password'], 'confirm_password': query['confirm_password']})

    return jsonify({'users': output})
        
#get a user by name
@app.route('/users/<string:name>', methods = ['GET'])
def get_user(name):
    users = mongo.db.users

    query = users.find_one({'name': name})
    if query:
        output = {'_id': str(query['_id']), 'name': query['name'], 'password': query['password'], 'confirm_password': query['confirm_password']}
    else:
        output = 'No results found'
    return jsonify({"user": output})

#verify if a user is registered
@app.route('/users/is_registered', methods = ['POST'])
def find_one():
    users = mongo.db.users

    if ('name' in request.json) and (request.json['name'] != '') and ('password' in request.json) and (request.json['password'] != ''):
        _name = request.json['name']    
        query = users.find_one({'name': _name})
        if query is not None:
            if ('password' in request.json) and (request.json['password'] != ''):
                if query['password'] == request.json['password']:
                    return jsonify({"response": "success", "message": ''})
                else:
                    return jsonify({"response": "fail", "message": "Wrong credentials!"})
            else:
                return jsonify({"response": "fail", "message": "Please provide both username and password!"})
        else:
            return jsonify({"response": "fail", "message": "This user is not registered."})
    else:
        return jsonify({"response": "fail", "message": "Please provide both username and password!"})
   
#create a user
@app.route('/create_user', methods = ['POST'])
def add_user():
    users = mongo.db.users

    if ('name' in request.json) and (request.json['name'] != ''):
        name = request.json['name']
    else:
        return jsonify({"response": "fail", "message": "Please provide both username and password!"})

    if ('password' in request.json) and (request.json['password'] != ''):
        password = request.json['password']
    else:
        return jsonify({"response": "fail", "message": "Please provide both username and password!"})

    if ('confirm_password' in request.json) and (request.json['confirm_password'] != ''):
        confirm_password = request.json['confirm_password']
    else:
        return jsonify({"response": "fail", "message": "Please confirm the password!"})

    query = users.find_one({'name': name}) 
    if query is not None:
        return jsonify({"response": "fail", "message": "Please provide another username"})

    if(password == confirm_password):
        if ('name' in request.json) and ('password' in request.json) and ('confirm_password' in request.json) and request.method == 'POST':
            users.insert_one({'name': name, 'password': password, 'confirm_password': confirm_password})

            return jsonify({"response" : "success", "message": 'User created successfully. Please log in!'})
    else:
        return jsonify({"response": "fail", "message": "Password and password confirmation don't match"})
 
#update a user
@app.route('/users/<id>', methods = ['PUT'])
def update_user(id):
    users = mongo.db.users

    if 'name' in request.json:
        name = request.json['name']
        query = users.find_one({'name': name}) 
        if query is not None:
            return jsonify({"response": "fail", "message": "Please provide another name"})
        else:
            users.update_one({'_id': ObjectId(id)}, {'$set': {'name': name}})

    if 'password' in request.json:
        password = request.json['password']
        users.update_one({'_id': ObjectId(id)}, {"$set": {"password": password}})

    if 'confirm_password' in request.json:
        confirm_password = request.json['confirm_password']
        users.update_one({'_id': ObjectId(id)}, {"$set": {"confirm_password": confirm_password}})
    
    return jsonify({"response" : "succes", "message" : "User updated successfully"})
    
#delete a user
@app.route('/users/<id>', methods = ['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    return jsonify({"response" : "succes", "message" : "User deleted successfully"})







#CONNECTIONS
#function to get all connections from a specific user
def get_connections_from_user(id):
    connections = mongo.db.connections
    user_connections = mongo.db.user_connections
    output = []

    user_connection_query = list(user_connections.find({'user_id': id}))
    print(user_connection_query, flush = True) 

    for item in user_connection_query:
        print(str(item['connection_id']), flush = True)
 
        connection_query = connections.find_one({'_id': ObjectId(str(item['connection_id'])) })
        print(connection_query, flush = True) 
        output.append({'_id': str(connection_query['_id']), 'name': connection_query['name'], 'type': connection_query['type'], 'admin_api_url': connection_query['admin_api_url']})
        
    return output

#function to get a connection by name for a specific user
def get_connection_by_name(user_id, name):
    connections_from_user = get_connections_from_user(user_id)
    print("ALO",  flush = True)
    print(name,  flush = True)
    output = {}
    for item in connections_from_user:
        print(item,  flush = True)
        if (item['name'] == name) :
            print(item['name'],  flush = True)
            output = {'_id': str(item['_id']), 'name': item['name'], 'type': item['type'], 'admin_api_url': item['admin_api_url']}
            return output
        
    return output

#function to get a connection by ID
def get_connection_by_ID(id):
    connections = mongo.db.connections
    output = {}
    
    query = connections.find_one({'_id': ObjectId(id)}) 
    if query:
        output = {'_id': str(query['_id']), 'name': query['name'], 'type': query['type'], 'admin_api_url': query['admin_api_url']}

    return output

#get all connections
@app.route('/connections', methods = ['GET'])
def get_connections():
    connections = mongo.db.connections      #the collection i have in my db
    output = []

    for query in connections.find():        #find all the documents in the collection    
        output.append({'_id': str(query['_id']), 'name': query['name'], 'type': query['type'], 'admin_api_url': query['admin_api_url']})

    return jsonify({'connections': output})

#get a connection by id *
@app.route('/connections/<id>', methods = ['GET'])
def get_connection_by_id(id):
    output = get_connection_by_ID(id)
    return jsonify({"connection": output})

#get all connections from a specific user *
@app.route('/users/<user_id>/connections', methods = ['GET'])
def get_user_connections(user_id):
    output = get_connections_from_user(user_id)
    return jsonify({'connections': output})

#get a connection by name for a specific user
@app.route('/users/<user_id>/connections/<name>', methods = ['GET'])
def get_connection(user_id, name):
    output = get_connection_by_name(user_id, name)
    return jsonify({"connection": output})
    
#delete a connection *
@app.route('/connections/<id>', methods = ['DELETE'])
def delete_connection(id):
    mongo.db.connections.delete_one({'_id': ObjectId(id)})
    return jsonify({"response" : "succes", "message" : "Connection deleted successfully"})

#get all user_connections dependencies
@app.route('/user_connections', methods = ['GET'])
def get_connections_dependency():
    connections = mongo.db.user_connections      #the collection i have in my db
    output = []

    for query in connections.find():        #find all the documents in the collection    
        output.append({'_id': str(query['_id']), 'connection_id': query['connection_id'], 'user_id': query['user_id'] })

    return jsonify({'connections': output})

#get user_connection dependency where id connection is...
@app.route('/user_connections/<connection_id>', methods = ['GET'])
def get_connection_user(connection_id):
    connections = mongo.db.user_connections
    output = []
    query = connections.find_one({'connection_id': connection_id})
    if query:
        output = {'_id': str(query['_id']), 'user_id': query['user_id'], 'connection_id': query['connection_id']}
    return jsonify({"dependency": output})

#create user-connection dependency
@app.route('/user_connections', methods = ['POST'])
def add_connection_dependency():
    connections = mongo.db.user_connections

    if ('connection_id' in request.json) and (request.json['connection_id'] != ''):
        connection_id = request.json['connection_id']
    else:
        return jsonify({"response": "fail", "message": "Please provide a connection_id!"})

    if ('user_id' in request.json) and (request.json['user_id'] != ''):
        user_id = request.json['user_id']
    else:
        return jsonify({"response": "fail", "message": "Please provide a user_id!"})


    if ('connection_id' in request.json) and ('user_id' in request.json) and request.method == 'POST':
        connections.insert_one({'connection_id': connection_id, 'user_id': user_id})
   
    return jsonify({"response" : "success", "message": 'User_connection dependency created successfully!'})

#delete a user_connection dependency
@app.route('/user_connections/<id>', methods = ['DELETE'])
def delete_connection_dependency(id):
    mongo.db.user_connections.delete_one({'_id': ObjectId(id)})
    return jsonify({"response" : "succes", "message" : "User_connection dependency deleted successfully"})

#create a connection for a specific user *
@app.route('/users/<user_id>/connections', methods = ['POST'])
def add_connection(user_id):
    connections = mongo.db.connections

    if ('name' in request.json) and (request.json['name'] != ''):
        name = request.json['name']
    else:
        return jsonify({"response": "fail", "message": "Please provide a name!"})

    if ('type' in request.json) and (request.json['type'] != ''):
        type = request.json['type']
    else:
        return jsonify({"response": "fail", "message": "Please provide a type!"})

    if ('admin_api_url' in request.json) and (request.json['admin_api_url'] != ''):
        admin_api_url = request.json['admin_api_url']  
    else:
        return jsonify({"response": "fail", "message": "Please provide an admin_api_url!"})


    print(user_id, flush = True )
    output = get_connections_from_user(user_id)
    print(output, flush = True )

    for i in range(len(output)):
        #print(i, flush = True )
        #print(output[i], flush = True )
        if (output[i]['name'] == name):
            return jsonify({"response": "fail", "message": "Please provide another name"})

    if ('name' in request.json) and ('type' in request.json) and ('admin_api_url' in request.json) and request.method == 'POST':
        connection_id = connections.insert_one({'name': name, 'type': type, 'admin_api_url': admin_api_url}).inserted_id 
   
    return jsonify({"response" : "success", "message": 'Connection created successfully!', 'new_connection_id': str(connection_id)})
 
#update a connection for a specific user * 
@app.route('/users/<user_id>/connections/<connection_id>', methods = ['PUT'])
def update_connection(user_id, connection_id):
    connections = mongo.db.connections

    if ('name' in request.json) and (request.json['name'] != ''):
        name = request.json['name']
    else:
        return jsonify({"response": "fail", "message": "Please provide a name!"})

    if ('type' in request.json) and (request.json['type'] != ''):
        type = request.json['type']
    else:
        return jsonify({"response": "fail", "message": "Please provide a type!"})

    if ('admin_api_url' in request.json) and (request.json['admin_api_url'] != ''):
        admin_api_url = request.json['admin_api_url']
    else:
        return jsonify({"response": "fail", "message": "Please provide an admin_api_url!"})

    if ('name' in request.json) and ('type' in request.json) and ('admin_api_url' in request.json) and request.method == 'PUT':
        output = get_connections_from_user(user_id)
        for i in range(len(output)):
            if (output[i]['name'] == name) and (output[i]['_id'] != connection_id):
                return jsonify({"response": "fail", "message": "Please provide another name"})
            else:
                connections.update_one({'_id': ObjectId(connection_id)}, {'$set': {'name': name}})
        
        connections.update_one({'_id': ObjectId(connection_id)}, {"$set": {"type": type}})
        
        connections.update_one({'_id': ObjectId(connection_id)}, {"$set": {"admin_api_url": admin_api_url}})

    return jsonify({"response" : "success", "message" : "Connection updated successfully"})









#SERVICES
#function to get all servicies from a specific connection
def get_servicies_from_connection(connection_id):
    connection_services = mongo.db.connection_services
    connection_admin_api_url = get_connection_by_ID(connection_id)['admin_api_url']
    output = []
    
    print(connection_admin_api_url, flush = True )
    print("ALO", flush = True )
    connection_service_query = list(connection_services.find({'connection_id': connection_id}))
    print(connection_service_query, flush = True) 
    
    for item in connection_service_query:
        print(str(item['service_id']), flush = True)
 
        res = requests.get(connection_admin_api_url + '/services/' + str(item['service_id']))
        dictFromServer = res.json()
        print(dictFromServer, flush = True )
        output.append(dictFromServer)

    return output

#get all services from a specific connection *
@app.route('/connections/<connection_id>/services', methods = ['GET'])
def get_connection_services(connection_id):
    output = get_servicies_from_connection(connection_id)       
    return jsonify({'services': output})

#get all services  ??
@app.route('/services', methods = ['GET'])
def get_services():
    res = requests.get('http://gw-kong:8001/services/')
    dictFromServer = res.json()
    print(dictFromServer, flush = True )
    return jsonify({"content": dictFromServer, "response": res.status_code })

#get a service by name *
@app.route('/connections/<connection_id>/services/<name>', methods = ['GET'])
def get_service_by_name(connection_id, name):
    connection_admin_api_url = get_connection_by_ID(connection_id)['admin_api_url']
    print(connection_admin_api_url, flush = True )
    print("ALO", flush = True )
    res = requests.get(connection_admin_api_url + '/services/' + name)
    dictFromServer = res.json()
    print(dictFromServer, flush = True )
    return jsonify({"content": dictFromServer, "response": res.status_code })

#create a service for a specific connection*
@app.route('/connections/<connection_id>/services', methods = ['POST'])
def create_service(connection_id):
    connection_admin_api_url = get_connection_by_ID(connection_id)['admin_api_url']
    print(connection_admin_api_url, flush = True )
    print("ALO", flush = True )


    if ('name' in request.json) and (request.json['name'] != ''):
        name = request.json['name']
    else:
        return jsonify({"response": "fail", "message": "Please provide a name!"})

    
    if ('path' in request.json) and (request.json['path'] != ''):
            path = request.json['path']
    else:
        return jsonify({"response": "fail", "message": "Please provide a path!"})

    if ('port' in request.json) and (request.json['port'] != ''):
            port = request.json['port']
    else:
        return jsonify({"response": "fail", "message": "Please provide a port!"})

    if ('host' in request.json) and (request.json['host'] != ''):
        host = request.json['host']
    else:
        return jsonify({"response": "fail", "message": "Please provide a host!"})
    
    
    if ('name' in request.json) and ('path' in request.json) and ('port' in request.json) and ('host' in request.json) and request.method == 'POST':
        dictToSend = {"name": name, "path": path, "port": port, "host": host}
    
        res = requests.post(connection_admin_api_url + '/services/', json = dictToSend)
        dictFromServer = res.json()
        print(dictFromServer, flush = True )

    return jsonify({"content": dictFromServer, "response": res.status_code })

#update a service for a specific connection *
@app.route('/connections/<connection_id>/services/<service_id>', methods = ['PUT'])
def update_service(connection_id, service_id):
    connection_admin_api_url = get_connection_by_ID(connection_id)['admin_api_url']

    if 'name' in request.json and (request.json['name'] != ''):
        name = request.json['name']
    else:
        return jsonify({"response": "fail", "message": "Please provide a name!"})

    if 'path' in request.json and (request.json['path'] != ''):
        path = request.json['path']
    else:
        return jsonify({"response": "fail", "message": "Please provide a path!"})

    if 'port' in request.json and (request.json['port'] != ''):
        port = request.json['port']
    else:
        return jsonify({"response": "fail", "message": "Please provide a port!"})

    if 'host' in request.json and (request.json['host'] != ''):
        host = request.json['host']
    else:
        return jsonify({"response": "fail", "message": "Please provide a host!"})

    if ( ('name' in request.json) or ('path' in request.json) or ('port' in request.json) or ('host' in request.json)) and request.method == 'PUT':
        dictToSend = {"name": name, "path": path, "port": port, "host": host}
    
        res = requests.put(connection_admin_api_url + '/services/' + service_id, json = dictToSend)
        dictFromServer = res.json()
        print(dictFromServer, flush = True)
    
    return jsonify({"content": dictFromServer, "response": res.status_code }) 

#delete a service *
@app.route('/connections/<connection_id>/services/<name>', methods = ['DELETE'])
def delete_service(connection_id, name):
    connection_admin_api_url = get_connection_by_ID(connection_id)['admin_api_url']
    res = requests.delete(connection_admin_api_url + '/services/' + name)
    
    if(res.status_code == 400) :
        dictFromServer = res.json()
        print(dictFromServer, flush = True )
        return jsonify({"content": dictFromServer, "response": res.status_code })
    else:
        return jsonify({"response": res.status_code })

#get all connection_services dependencies 
@app.route('/connection_services', methods = ['GET'])
def get_services_dependency():
    services = mongo.db.connection_services      #the collection i have in my db
    output = []

    for query in services.find():        #find all the documents in the collection    
        output.append({'_id': str(query['_id']), 'service_id': query['service_id'], 'connection_id': query['connection_id'] })

    return jsonify({'services': output})

#get connection_service dependency where id service is...
@app.route('/connection_services/<service_id>', methods = ['GET'])
def get_connection_service(service_id):
    connections = mongo.db.connection_services

    query = connections.find_one({'service_id': service_id})
    if query:
        output = {'_id': str(query['_id']), 'service_id': query['service_id'], 'connection_id': query['connection_id']}
    else:
        output = 'No results found'
    return jsonify({"dependency": output})

#create connection-service dependency
@app.route('/connection_services', methods = ['POST'])
def add_service_dependency():
    services = mongo.db.connection_services

    if ('service_id' in request.json) and (request.json['service_id'] != ''):
        service_id = request.json['service_id']
    else:
        return jsonify({"response": "fail", "message": "Please provide a service_id!"})

    if ('connection_id' in request.json) and (request.json['connection_id'] != ''):
        connection_id = request.json['connection_id']
    else:
        return jsonify({"response": "fail", "message": "Please provide a connection_id!"})


    if ('service_id' in request.json) and ('connection_id' in request.json) and request.method == 'POST':
        connection_service_id = services.insert_one({'service_id': service_id, 'connection_id': connection_id}).inserted_id    #generates a random id
        new_service = services.find_one({'_id': connection_service_id})
        #output = {'service_id': new_service['service_id'], 'connection_id': new_service['connection_id']}
   
        return jsonify({"response" : "success", "message": 'connection_service dependency created successfully!'})

#delete a connection_service dependency
@app.route('/connection_services/<id>', methods = ['DELETE'])
def delete_service_dependency(id):
    mongo.db.connection_services.delete_one({'_id': ObjectId(id)})
    return jsonify({"response" : "succes", "message" : "connection_service dependency deleted successfully"})









#ROUTES
#function to get all routes from a specific connection
def get_routes_from_connection(connection_id):
    connection_routes = mongo.db.connection_routes
    connection_admin_api_url = get_connection_by_ID(connection_id)['admin_api_url']
    output = []

    connection_route_query = list(connection_routes.find({'connection_id': connection_id}))
    print(connection_route_query, flush = True) 
    
    for item in connection_route_query:
        print(str(item['route_id']), flush = True)
 
        res = requests.get(connection_admin_api_url + '/routes/'+ str(item['route_id']))
        dictFromServer = res.json()
        print(dictFromServer, flush = True )
        output.append(dictFromServer)
        
    return output

#function to get a route by id
def get_route_by_ID(connection_id, route_id):
    connection_admin_api_url = get_connection_by_ID(connection_id)['admin_api_url']
    res = requests.get(connection_admin_api_url + '/routes/' + route_id)
    dictFromServer = res.json()
    print(dictFromServer, flush = True )
    return dictFromServer

#get all routes
@app.route('/routes', methods = ['GET'])
def get_routes():
    res = requests.get('http://gw-kong:8001/routes/')
    dictFromServer = res.json()
    print(dictFromServer, flush = True )
    return jsonify({"content": dictFromServer, "response": res.status_code })

#get a route by name
@app.route('/connections/<connection_id>/routes/<name>', methods = ['GET'])
def get_route_by_name(connection_id, name):
    connection_admin_api_url = get_connection_by_ID(connection_id)['admin_api_url']
    res = requests.get(connection_admin_api_url + '/routes/' + name)
    dictFromServer = res.json()
    print(dictFromServer, flush = True )
    return jsonify({"content": dictFromServer, "response": res.status_code })

#get all routes from a specific connection * 
@app.route('/connections/<connection_id>/routes', methods = ['GET'])
def get_connection_routes(connection_id):
    output = get_routes_from_connection(connection_id)
        
    return jsonify({'routes': output})

#create a route for a specific connection *
@app.route('/connections/<connection_id>/routes', methods = ['POST'])
def create_route(connection_id):
    connection_admin_api_url = get_connection_by_ID(connection_id)['admin_api_url']
    routes = get_routes_from_connection(connection_id)

    if ('name' in request.json) and (request.json['name'] != ''):
        name = request.json['name']
    else:
        return jsonify({"response": "fail", "message": "Please provide a name!"})

    if ('paths' in request.json) and (request.json['paths'] != ''):
        if routes:
            for item in routes:
                if(request.json['paths'] != item['paths']):
                    paths = request.json['paths']
                else:
                    return jsonify({"response": "fail", "message": "Please provide another path!"})    
        else:
            paths = request.json['paths']
    else:
        return jsonify({"response": "fail", "message": "Please provide at least a path!"})

   
    if ('service' in request.json) and (request.json['service'] != ''):
        service = request.json['service']
    else:
        return jsonify({"response": "fail", "message": "Please provide a service!"})

    
    if ('name' in request.json) and ('paths' in request.json) and ('service' in request.json) and request.method == 'POST':
        dictToSend = {"name": name, "paths": paths, "service": service}
    
        res = requests.post(connection_admin_api_url + '/routes/', json = dictToSend)
        dictFromServer = res.json()
        print(dictFromServer, flush = True )

    return jsonify({"content": dictFromServer, "response": res.status_code })

#update a route *
@app.route('/connections/<connection_id>/routes/<route_id>', methods = ['PUT'])
def update_route(connection_id, route_id):
    connection_admin_api_url = get_connection_by_ID(connection_id)['admin_api_url']
    routes = get_routes_from_connection(connection_id)
    current_route = get_route_by_ID(connection_id, route_id)

    if 'name' in request.json and (request.json['name'] != ''):
        name = request.json['name']
    else:
        return jsonify({"response": "fail", "message": "Please provide a name!"})

    if ('paths' in request.json) and (request.json['paths'] != ''):
        if routes:
            for item in routes:
                if item != current_route:
                    if(request.json['paths'] != item['paths']):
                        paths = request.json['paths']
                    else:
                        return jsonify({"response": "fail", "message": "Please provide another path!"})    
                else:
                    paths = request.json['paths']
        else:
            paths = request.json['paths']
    else:
        return jsonify({"response": "fail", "message": "Please provide at least a path!"})

    if 'service' in request.json and (request.json['service'] != ''):
        service = request.json['service']
    else:
        return jsonify({"response": "fail", "message": "Please provide a service ID!"})

    if (('name' in request.json) or ('paths' in request.json) or ('service' in request.json)) and request.method == 'PUT':
        dictToSend = { "name": name, "paths": paths, "service": service}
    
        res = requests.put(connection_admin_api_url + '/routes/' + route_id, json = dictToSend)
        dictFromServer = res.json()
        print(dictFromServer, flush = True )
       
    return jsonify({"content": dictFromServer, "response": res.status_code })

#delete a route *
@app.route('/connections/<connection_id>/routes/<name>', methods = ['DELETE'])
def delete_route(connection_id, name):
    connection_admin_api_url = get_connection_by_ID(connection_id)['admin_api_url']
    print(name, flush = True )
    res = requests.delete(connection_admin_api_url + '/routes/' + name)
    return jsonify({"response": res.status_code})

#get all connection_routes dependencies
@app.route('/connection_routes', methods = ['GET'])
def get_routes_dependency():
    routes = mongo.db.connection_routes      #the collection i have in my db
    output = []

    for query in routes.find():        #find all the documents in the collection    
        output.append({'_id': str(query['_id']), 'route_id': query['route_id'], 'connection_id': query['connection_id'] })

    return jsonify({'routes': output})

#create connection-route dependency
@app.route('/connection_routes', methods = ['POST'])
def add_route_dependency():
    routes = mongo.db.connection_routes

    if ('route_id' in request.json) and (request.json['route_id'] != ''):
        route_id = request.json['route_id']
    else:
        return jsonify({"response": "fail", "message": "Please provide a route_id!"})

    if ('connection_id' in request.json) and (request.json['connection_id'] != ''):
        connection_id = request.json['connection_id']
    else:
        return jsonify({"response": "fail", "message": "Please provide a connection_id!"})


    if ('route_id' in request.json) and ('connection_id' in request.json) and request.method == 'POST':
        connection_route_id = routes.insert_one({'route_id': route_id, 'connection_id': connection_id}).inserted_id    #generates a random id
        new_route = routes.find_one({'_id': connection_route_id})
        #output = {'route_id': new_route['route_id'], 'connection_id': new_route['connection_id']}
   
        return jsonify({"response" : "success", "message": 'connection_route dependency created successfully!'})

#get connection_route dependency where id route is...
@app.route('/connection_routes/<route_id>', methods = ['GET'])
def get_connection_route(route_id):
    connections = mongo.db.connection_routes

    query = connections.find_one({'route_id': route_id})
    if query:
        output = {'_id': str(query['_id']), 'route_id': query['route_id'], 'connection_id': query['connection_id']}
    else:
        output = 'No results found'
    return jsonify({"dependency": output})

#delete a connection_route dependency
@app.route('/connection_routes/<id>', methods = ['DELETE'])
def delete_route_dependency(id):
    mongo.db.connection_routes.delete_one({'_id': ObjectId(id)})
    return jsonify({"response" : "succes", "message" : "connection_route dependency deleted successfully"})







#TYK
#function to get all apis for a specific connection
def get_tyk_apis(connection_id):
    connection_tyk_apis = mongo.db.connection_tyk_apis
    connection_admin_api_url = get_connection_by_ID(connection_id)['admin_api_url']
    output = []
    print(connection_admin_api_url, flush = True )
    print("ALO", flush = True )

    connection_tyk_api_query = list(connection_tyk_apis.find({'connection_id': connection_id}))
    print(connection_tyk_api_query, flush = True)

    if connection_tyk_api_query:
        for item in connection_tyk_api_query:
            print(item['tyk_api_id'], flush = True)
        
            res = requests.get(connection_admin_api_url + '/tyk/apis/' + item['tyk_api_id'], headers={"x-tyk-authorization":"352d20ee67be67f6340b4c0605b044b7"})
            dictFromServer = res.json()
            print(dictFromServer, flush = True )
            output.append(dictFromServer)

    return output

#function to do reload
def reload(connection_id):
    connection_admin_api_url = get_connection_by_ID(connection_id)['admin_api_url']
    print(connection_admin_api_url, flush = True )
    print("ALO", flush = True )
    
    res = requests.get(connection_admin_api_url + '/tyk/reload', headers={"x-tyk-authorization":"352d20ee67be67f6340b4c0605b044b7"})
    dictFromServer = res.json()
    print(dictFromServer, flush = True )

    time.sleep(1.5)
    return dictFromServer

#function to get api by id
def get_api_by_id(connection_id, tyk_api_id):
    connection_admin_api_url = get_connection_by_ID(connection_id)['admin_api_url']
    print(connection_admin_api_url, flush = True )
    print("ALO", flush = True )
    
    res = requests.get(connection_admin_api_url + '/tyk/apis/' + tyk_api_id, headers={"x-tyk-authorization":"352d20ee67be67f6340b4c0605b044b7"})

    return res

#reload
@app.route('/connections/<connection_id>/tyk/reload', methods = ['GET'])
def do_reload(connection_id):
    dictFromServer = reload(connection_id)
    
    return jsonify({'content': dictFromServer})

#get all apis
@app.route('/tyk/apis', methods = ['GET'])
def get_all_tyk_apis():
    res = requests.get('http://gw-tyk:8080//tyk/apis/', headers={"x-tyk-authorization":"352d20ee67be67f6340b4c0605b044b7"})
    dictFromServer = res.json()
    print(dictFromServer, flush = True )
    return jsonify({"content": dictFromServer, "response": res.status_code })

#get all apis for a specific connection
@app.route('/connections/<connection_id>/tyk/apis', methods = ['GET'])
def get_all_tyk_apis_per_connection(connection_id):
    dictFromServer = get_tyk_apis(connection_id)
    return jsonify({'content': dictFromServer})

#get api by id
@app.route('/connections/<connection_id>/tyk/apis/<tyk_api_id>', methods = ['GET'])
def get_tyk_api_by_id(connection_id, tyk_api_id):
    res = get_api_by_id(connection_id, tyk_api_id)
    dictFromServer = res.json()
    print(dictFromServer, flush = True )
    
    return jsonify({'content': dictFromServer, "response": res.status_code})

#create api
@app.route('/connections/<connection_id>/tyk/apis', methods = ['POST'])
def create_tyk_api(connection_id):
    connection_admin_api_url = get_connection_by_ID(connection_id)['admin_api_url']
    print(connection_admin_api_url, flush = True )
    print("ALO", flush = True )

    tyk_apis = get_tyk_apis(connection_id)
    print(tyk_apis, flush = True )
    
    print(request.json, flush = True )

    if ('name' in request.json) and (request.json['name'] != ''):
        name = request.json['name']   
    else:
        return jsonify({"response": "fail", "message": "Please provide a name!"})

    if ('api_id' in request.json) and (request.json['api_id'] != ''):
        if tyk_apis:
            for item in tyk_apis:
                if(request.json['name'] != item['api_id']):
                    api_id = request.json['name']
                else:
                    return jsonify({"response": "fail", "message": "Please provide another name!"})
        else: 
            api_id = request.json['name']
    else:
        return jsonify({"response": "fail", "message": "Please provide a name!"})
       
    if ('proxy' in request.json) and (request.json['proxy'] != ''):
        proxy = request.json['proxy']
    else:
        return jsonify({"response": "fail", "message": "Please provide a proxy!"})

    if ('listen_path' in request.json['proxy']) and (request.json['proxy']['listen_path'] != ''):
        if tyk_apis:
            for item in tyk_apis:
                if(request.json['proxy']['listen_path'] != item['proxy']['listen_path']):
                    listen_path = request.json['proxy']['listen_path']
                else:
                    return jsonify({"response": "fail", "message": "Please provide another route_path!"})
        else:
            listen_path = request.json['proxy']['listen_path'] 
    else:
        return jsonify({"response": "fail", "message": "Please provide a route_path!"})

    if ('target_url' in request.json['proxy']) and (request.json['proxy']['target_url'] != ''):
        target_url = request.json['proxy']['target_url']
    else:
        return jsonify({"response": "fail", "message": "Please provide a target_url!"})
    
    
    if ('name' in request.json) and ('api_id' in request.json) and ('proxy' in request.json) and ('listen_path' in request.json['proxy']) and ('target_url' in request.json['proxy']) and request.method == 'POST':
        dictToSend = {
            "name": name,
            "api_id": api_id,
            "org_id": "default",
            "definition": {
                "location": "header",
                "key": "version"
            },
            "use_keyless": True,
            "version_data": {
                "not_versioned": True,
                "versions": {
                    "Default": {
                        "name": "Default"
                    }
                }
            },
            "custom_middleware": {
                "pre": [
                    {
                        "name": "testJSVMData",
                        "path": "./middleware/injectHeader.js",
                        "require_session": False,
                        "raw_body_only": False
                    }
                ]
            },
            "driver": "otto",
            "proxy": {
                "listen_path": listen_path,
                "target_url": target_url,
                "strip_listen_path": True
            }
        }

        res = requests.post(connection_admin_api_url + '/tyk/apis', json = dictToSend, headers={"x-tyk-authorization":"352d20ee67be67f6340b4c0605b044b7"})
        dictFromServer = res.json()
        print(dictFromServer, flush = True )

        reload(connection_id)
        
    
        return jsonify({'content': dictFromServer, "response": res.status_code})

#update api
@app.route('/connections/<connection_id>/tyk/apis/<tyk_api_id>', methods = ['PUT'])
def update_tyk_api(connection_id, tyk_api_id):
    connection_admin_api_url = get_connection_by_ID(connection_id)['admin_api_url']
    print(connection_admin_api_url, flush = True )
    print("ALO", flush = True )
    print("request.json", flush = True )
    print(request.json, flush = True )
    
    tyk_apis = get_tyk_apis(connection_id)
    print(tyk_apis, flush = True )

    resp = get_api_by_id(connection_id, tyk_api_id)
    current_api = resp.json()
    print(current_api, flush = True )
    
    if ('name' in request.json) and (request.json['name'] != ''):
        name = request.json['name']
    else:
        return jsonify({"response": "fail", "message": "Please provide a name!"})

    if ('api_id' in request.json) and (request.json['api_id'] != ''):
        if(request.json['api_id'] == tyk_api_id):
            api_id = request.json['api_id']
        else:
            return jsonify({"response": "fail", "message": "Please don't modify the name!"})
    else:
        return jsonify({"response": "fail", "message": "Please provide a name!"})

    if ('proxy' in request.json) and (request.json['proxy'] != ''):
        proxy = request.json['proxy']
    else:
        return jsonify({"response": "fail", "message": "Please provide a proxy!"})

    if ('listen_path' in request.json['proxy']) and (request.json['proxy']['listen_path'] != ''):
        if tyk_apis:
            for item in tyk_apis:
                print("item", flush = True )
                print(item, flush = True )
                if(item != current_api):
                    if(request.json['proxy']['listen_path'] != item['proxy']['listen_path']):
                        listen_path = request.json['proxy']['listen_path']
                    else:
                        return jsonify({"response": "fail", "message": "Please provide another listen_path!"})  
                else:
                    listen_path = request.json['proxy']['listen_path']  
        else:
            listen_path = request.json['proxy']['listen_path']
    else:
        return jsonify({"response": "fail", "message": "Please provide a listen_path!"})

    if ('target_url' in request.json['proxy']) and (request.json['proxy']['target_url'] != ''):
        target_url = request.json['proxy']['target_url']
    else:
        return jsonify({"response": "fail", "message": "Please provide a target_url!"})
    
    
    if ('name' in request.json) and ('api_id' in request.json) and ('proxy' in request.json) and ('listen_path' in request.json['proxy']) and ('target_url' in request.json['proxy']) and request.method == 'PUT':
        dictToSend = {
            "name": name,
            "api_id": api_id,
            "org_id": "default",
            "definition": {
                "location": "header",
                "key": "version"
            },
            "use_keyless": True,
            "version_data": {
                "not_versioned": True,
                "versions": {
                    "Default": {
                        "name": "Default"
                    }
                }
            },
            "custom_middleware": {
                "pre": [
                    {
                        "name": "testJSVMData",
                        "path": "./middleware/injectHeader.js",
                        "require_session": False,
                        "raw_body_only": False
                    }
                ]
            },
            "driver": "otto",
            "proxy": {
                "listen_path": listen_path,
                "target_url": target_url,
                "strip_listen_path": True
            }
        }

        res = requests.put(connection_admin_api_url + '/tyk/apis/' + tyk_api_id, json = dictToSend, headers={"x-tyk-authorization":"352d20ee67be67f6340b4c0605b044b7"})
        dictFromServer = res.json()
        print(dictFromServer, flush = True )

        reload(connection_id)
    
        return jsonify({'content': dictFromServer, "response": res.status_code})

#delete api
@app.route('/connections/<connection_id>/tyk/apis/<tyk_api_id>', methods = ['DELETE'])
def delete_tyk_api_by_id(connection_id, tyk_api_id):
    connection_admin_api_url = get_connection_by_ID(connection_id)['admin_api_url']
    print(connection_admin_api_url, flush = True )
    print("ALO", flush = True )
    
    res = requests.delete(connection_admin_api_url + '/tyk/apis/' + tyk_api_id, headers={"x-tyk-authorization":"352d20ee67be67f6340b4c0605b044b7"})
    dictFromServer = res.json()
    print(dictFromServer, flush = True )

    reload(connection_id)
    
    return jsonify({'content': dictFromServer, "response": res.status_code})

#get all connection_tyk_apis dependencies
@app.route('/connection_tyk_apis', methods = ['GET'])
def get_tyk_apis_dependency():
    tyk_apis = mongo.db.connection_tyk_apis      #the collection i have in my db
    output = []

    for query in tyk_apis.find():        #find all the documents in the collection    
        output.append({'_id': str(query['_id']), 'tyk_api_id': query['tyk_api_id'], 'connection_id': query['connection_id'] })

    return jsonify({'tyk_apis': output})

#create connection-tyk_api dependency
@app.route('/connection_tyk_apis', methods = ['POST'])
def add_tyk_api_dependency():
    tyk_apis = mongo.db.connection_tyk_apis

    if ('tyk_api_id' in request.json) and (request.json['tyk_api_id'] != ''):
        tyk_api_id = request.json['tyk_api_id']
    else:
        return jsonify({"response": "fail", "message": "Please provide a tyk_api_id!"})

    if ('connection_id' in request.json) and (request.json['connection_id'] != ''):
        connection_id = request.json['connection_id']
    else:
        return jsonify({"response": "fail", "message": "Please provide a connection_id!"})


    if ('tyk_api_id' in request.json) and ('connection_id' in request.json) and request.method == 'POST':
        connection_tyk_api_id = tyk_apis.insert_one({'tyk_api_id': tyk_api_id, 'connection_id': connection_id}).inserted_id    #generates a random id
        new_tyk_api = tyk_apis.find_one({'_id': connection_tyk_api_id})
        #output = {'tyk_api_id': new_tyk_api['tyk_api_id'], 'connection_id': new_tyk_api['connection_id']}
   
        return jsonify({"response" : "success", "message": 'connection_tyk_api dependency created successfully!'})

#get connection_tyk_api dependency where id tyk_api is...
@app.route('/connection_tyk_apis/<tyk_api_id>', methods = ['GET'])
def get_connection_tyk_api(tyk_api_id):
    connections = mongo.db.connection_tyk_apis

    query = connections.find_one({'tyk_api_id': tyk_api_id})
    if query:
        output = {'_id': str(query['_id']), 'tyk_api_id': query['tyk_api_id'], 'connection_id': query['connection_id']}
    else:
        output = 'No results found'
    return jsonify({"dependency": output})

#delete a connection_tyk_api dependency
@app.route('/connection_tyk_apis/<id>', methods = ['DELETE'])
def delete_tyk_api_dependency(id):
    mongo.db.connection_tyk_apis.delete_one({'_id': ObjectId(id)})
    return jsonify({"response" : "succes", "message" : "connection_tyk_api dependency deleted successfully"})




#KUBERNETES/DOCKER DEPLOYMENT
@app.route('/kubernetes/<connection_type>', methods = ['POST'])
def deployment(connection_type):
    file = ""
    if( connection_type == "kong"):
        file = "kong.yaml"
        
        with open(file) as kong_yaml: #deschide fisierul in variabila kong_yaml de tipul fisier object
            temp_kong = kong_yaml.read() #string -> e o lista de linii, fiecare linie e un string
            contor = mongo.db.contor
            contorKong = contor.find_one({"_id": ObjectId("62b217c06b7f9c0008198ac3")})
            print(contorKong, flush = True )
            contor_kong = contorKong['contor_kong']
            print(contor_kong, flush = True )
            if contor_kong == 1000:
                return jsonify({"response" : "fail", "message" : "Out of limit!"})
            
            print("\n\n------------------------\n\n", flush = True )
            temp_kong = temp_kong.replace("{{pg_port}}", str(40000 + contor_kong))
            temp_kong = temp_kong.replace("{{port1}}", str(41000 + contor_kong) )
            temp_kong = temp_kong.replace("{{port2}}", str(42000 + contor_kong) )
            temp_kong = temp_kong.replace("{{port3}}", str(43000 + contor_kong) )
            temp_kong = temp_kong.replace("{{port4}}", str(44000 + contor_kong) )

            print(temp_kong,  flush = True )
            new_file = str(contor_kong)+file

            with open(new_file, "w") as new_kong_yaml:
                new_kong_yaml.write(temp_kong)

            os.system('./kubectl create namespace kong' + str(contor_kong)) 
            os.system('./kubectl apply -f ' + new_file + " -n kong" + str(contor_kong))

            port = 43000 + contor_kong
            mongo.db.contor.update_one({'_id': ObjectId("62b217c06b7f9c0008198ac3")}, {"$inc": {'contor_kong': 1}} ) # -> increment the value
            return jsonify({"response" : "succes", "message" : "", "port": str(port), "contor": str(contor_kong)})



    elif( connection_type == "tyk"):
        file = "run_tyk.sh"
        with open(file) as tyk_yaml: #deschide fisierul in variabila tyk_yaml de tipul fisier object
            temp_tyk = tyk_yaml.read() #string
            contor = mongo.db.contor
            contorTyk = contor.find_one({"_id": ObjectId("62b217c06b7f9c0008198ac3")})
            print(contorTyk, flush = True )
            contor_tyk = contorTyk['contor_tyk']
            print(contor_tyk, flush = True )
            if contor_tyk == 1000:
                return jsonify({"response" : "fail", "message" : "Out of limit!"})
            
            print("\n\n------------------------\n\n", flush = True )
            temp_tyk = temp_tyk.replace("{{port1}}", str(44000 + contor_tyk) )
            #temp_tyk = temp_tyk.replace("{{redis_port}}", str(58000 + contor_tyk) )

            print(temp_tyk,  flush = True )
            new_file = str(contor_tyk)+file

            with open(new_file, "w") as new_tyk_yaml:
                new_tyk_yaml.write(temp_tyk)

            os.chmod(new_file, 0o0777) #il face exec ii da toate drepturile
            os.system('./' + new_file) 
            
            port = 44000 + contor_tyk
            mongo.db.contor.update_one({'_id': ObjectId("62b217c06b7f9c0008198ac3")}, {"$inc": {'contor_tyk': 1}} ) # -> increment the value

            return jsonify({"response" : "succes", "message" : "", "port": str(port), "contor": str(contor_tyk)})
    

    return jsonify({"response" : "fail", "message" : "Something went wrong!"})







if __name__ == '__main__':
    app.run(debug = False, host='0.0.0.0')
