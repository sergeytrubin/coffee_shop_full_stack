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

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()


## ROUTES

'''
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
def retrieve_all_drinks_short():
        """"Get request to retrieve all drinks"""

        # Retrieve all drinks
        selection = Drink.query.all()

        # Abort with 404 if no results found
        if len(selection) == 0:
            abort(404)

        # Add drinks to list
        drinks = [drink.short() for drink in selection]

        # Return data in JSON format
        return jsonify({
            'success': True,
            'drinks': drinks
        })


'''
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def retrieve_all_drinks_details(jwt):
        """"Get request to retrieve details of all drinks"""

        # Retrieve all drinks
        selection = Drink.query.all()

        # Abort with 404 if no results found
        if len(selection) == 0:
            abort(404)

        # Add drinks to list
        drinks = [drink.long() for drink in selection]

        # Return data in JSON format
        return jsonify({
            'success': True,
            'drinks': drinks
        })

'''
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
    """Post request to create new drink"""

    # Get the new question data from the form
    body = request.get_json()

    #Format new question
    new_title = body.get('title')
    new_recipe = body.get('recipe')

    try:
        # POST the new question to database
        drink = Drink(
            title=new_title,
            recipe=json.dumps(new_recipe)
        )
        drink.insert()

        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    # Abort 422 if create could not be processed
    except Exception as err:
        print(f"ERROR: {err}")
        abort(422)

'''
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(jwt, id):
    """Update drink details"""

    body = request.get_json()

    try:
        # Retrieve a drink by id
        drink = Drink.query.filter(Drink.id == id).one_or_none()

        # Abort 404 if result is None
        if drink is None:
            abort(404)

        # Retrieve the title if exist in body
        if 'title' in body:
            drink.title = body.get('title')
        
        # Retrieve the recipe if exist in body
        if 'recipe' in body:
            drink.recipe = json.dumps(body.get('recipe'))

        # Update the drink
        drink.update()

        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    # Abort 422 if update could not be processed
    except Exception as err:
        print(f"ERROR: {err}")
        abort(422)

'''
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, id):
    """Delete drink by id"""

    try:
        # Retrieve a drink by id
        drink = Drink.query.filter(
            Drink.id == id).one_or_none()

        # Abort 404 if result is None
        if drink is None:
            abort(404)

        # Delete the question
        drink.delete()

        # Return data in JSON format
        return jsonify({
            'success': True,
            'deleted': id
        })

    # Abort 422 if delete could not be processed
    except Exception as err:
        print(f"ERROR: {err}")
        abort(422)

## Error Handling

@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "not found"
    }), 404


@app.errorhandler(422)
def unprocessable_error(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

