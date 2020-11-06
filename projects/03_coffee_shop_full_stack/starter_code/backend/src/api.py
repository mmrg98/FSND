import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

db_drop_and_create_all()


'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''


## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['GET'])
def get_drinks():
    '''r="{'color': 'red', 'parts': 2},{'color': 'blue', 'parts': 2}"
    s=r.split(",")
    t=Drink(title="cap", recipe= r)
    t.insert()'''
    all_drinks = Drink.query.all()
    drinks = [drink.short() for drink in all_drinks]

    return jsonify(
             {"success": True,
              "drinks": drinks}
        )

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drink(test):
    all_drinks = Drink.query.all()
    drinks = [drink.long() for drink in all_drinks]
    return jsonify({
            'success': True,
            'drinks': drinks
        })

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink(jwt):
    try:
        recipe=''
        title = request.json['title']

        recipe = json.dumps(request.json['recipe'])
        recipe_json=json.loads(recipe)
        new_drink = Drink(title=title, recipe=recipe)
        new_drink.insert()

        return jsonify({
        "success": True,
        'drinks': new_drink.long()
        })

    except:
        abort(422)

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>/', methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_drink(jwt,drink_id):
    try:
        drink = Drink.query.get(drink_id)
        title = request.json['title']
        recipe = json.dumps(request.json['recipe'])
        recipe_json = json.loads(recipe)
        drink.title = title
        drink.recipe = recipe
        drink.update()

        return jsonify({
        "success": True,
        'drinks': drink.long()
        })

    except:
        abort(422)


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>/', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt,drink_id):
    try:
        drink = Drink.query.get(drink_id)
        drink.delete()

        return jsonify({
        "success": True,
        'delete': drink.id
        })

    except:
        abort(422)

## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
                    "success": False,
                    "error": 400,
                    "message": "bad request"
                    }), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
                    "success": False,
                    "error": 401,
                    "message": "unauthorized"
                    }), 401

@app.errorhandler(500)
def server_error(error):
    return jsonify({
                    "success": False,
                    "error": 500,
                    "message": "Internal server erro"
                    }), 500

@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
                    "success": False,
                    "error": AuthError,
                    "message": "Authentication Error"
                    }), AuthError




'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
