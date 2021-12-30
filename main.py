from flask import jsonify, abort
from paypal_order import CreateOrder
import os
from dotenv import load_dotenv

load_dotenv()


def main(request):

    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)
    elif request.method in ['GET', 'PUT', 'DELETE']:
        return abort(405)
    # else, it's a POST


    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    debug = 'debug' in os.environ

    data = request.json
    gcp_email = data['gcp_email']
    paypal_mode = data['paypal_mode']
    create_order_response = CreateOrder(mode=paypal_mode).create_order(gcp_email, debug=debug)

    response = jsonify({'id': create_order_response.result.id })

    return response, 200, headers
