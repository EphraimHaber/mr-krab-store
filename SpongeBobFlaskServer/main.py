from flask import Flask, jsonify, request
from flask_cors import CORS
import jsonschema
from jsonschema import validate
import asyncio

app = Flask(__name__)
CORS(app, origins='*')

menu = {
    'krabby_patty': {
        'name': 'Krabby Patty',
        'price': 3.99,
        'description': "The star of the Krusty Krab's menu, this burger is a legend in Bikini Bottom. Packed with "
                       "fresh lettuce, tomatoes, onions, and the secret Krabby Patty sauce, it's a must-try for "
                       "anyone visiting the Krusty Krab.",
        'id': 1
    },
    'krusty_krab_pizza': {
        'name': 'Krusty Krab Pizza',
        'price': 5.99,
        'description': "A delicious pizza made with fresh dough, sauce, and toppings, all cooked to perfection in the "
                       "Krusty Krab's oven. It's a hit with pizza lovers and SpongeBob fans alike!",
        'id': 2
    },
    'chum_burger': {
        'name': 'Chum Burger',
        'price': 2.99,
        'description': "The ultimate delicacy for the most adventurous eaters. Made from the finest chum, this burger "
                       "is a treat for the taste buds.",
        'id': 3
    },
    'kelp_fries': {
        'name': 'Kelp Fries',
        'price': 1.99,
        'description': 'A classic Krusty Krab side dish. Crunchy, salty, and a perfect complement to any Krabby Patty.',
        'id': 4
    },
}

item_schema = {
    "type": "object",
    "properties": {
        "description": {"type": "string"},
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "price": {"type": "number"},
        "quantity": {"type": "integer"}
    },
    "required": ["description", "id", "name", "price", "quantity"]
}


def is_valid_list(items: list) -> bool:
    # Validate each item in the list against the schema
    for item in items:
        try:
            validate(item, item_schema)
        except jsonschema.exceptions.ValidationError:
            return False

    # If all items are valid, return True
    return True


async def get_menu_with_delay():
    await asyncio.sleep(5)  # Sleep for 5 seconds
    return jsonify({'items': menu})


@app.route('/menu', methods=['GET'])
async def get_menu():
    menu = await get_menu_with_delay()
    return menu


@app.route('/orders', methods=['POST'])
def handle_orders():
    try:
        data = request.get_json()

        # Validate the order data
        if not data or 'items' not in data:
            raise ValueError('Invalid order data')

        if type(data['items']) is not list:
            print(type(data['items']))
            raise ValueError('Invalid data. is not list')

        if not is_valid_list(data['items']):
            raise ValueError('Invalid data sent, not all items are valid')

        has_positive_quantity = any(item['quantity'] > 0 for item in data['items'])

        if not has_positive_quantity:
            raise ValueError('At least one quantity should be greater then zero!.')

        # Process the order data here
        print(f'Received order: \n{data}')
        print(data['items'])

        app.config['latest_order'] = data
        response_data = {'success': True, 'message': 'Order successfully processed'}
        status_code = 200
    except ValueError as ve:
        print(f'Error processing order: {ve}')
        response_data = {'success': False, 'message': str(ve)}
        status_code = 400
    except Exception as e:
        print(f'Error processing order: {e}')
        response_data = {'success': False, 'message': 'Error processing order'}
        status_code = 500

    return jsonify(response_data), status_code


@app.route('/latest-order')
def get_latest_order():
    try:
        latest_order = app.config['latest_order']
    except KeyError:
        latest_order = None
    if not latest_order:
        response_data = {'success': False, 'message': 'No order placed'}
        status_code = 404
        return jsonify(response_data), status_code
    status_code = 200
    return jsonify(app.config['latest_order']), status_code


@app.route('/hello', methods=['GET'])
def get_hello():
    response_data = {'Hello': 'World'}
    status_code = 200
    return jsonify(response_data), status_code


if __name__ == '__main__':
    app.run(port=8000)
    app.config['latest_order'] = None
