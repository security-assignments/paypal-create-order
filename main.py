from flask import jsonify, abort
from paypal_order import CreateOrder
import os
import yaml
from dotenv import load_dotenv

load_dotenv()

env_file = "env.yml"
if os.environ.get("LOCAL_DEV"):
    if os.path.exists(env_file):
        with open(env_file) as f:
            env_vars = yaml.safe_load(f)
        for key, value in env_vars.items():
            os.environ[key] = str(value)


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

    kwargs = {}

    debug = 'debug' in os.environ
    kwargs["debug"] = debug

    data = request.json
    gcp_email = data['gcp_email']
    paypal_mode = data['paypal_mode']

    amount = False

    if "amount" in os.environ:
        amount = os.environ.get("amount")
        
    if paypal_mode == "SANDBOX":
        if "SANDBOX_AMOUNT" in os.environ:
            amount = os.environ.get("SANDBOX_AMOUNT")
    elif paypal_mode == "LIVE":
        if "LIVE_AMOUNT" in os.environ:
            amount = os.environ.get("LIVE_AMOUNT")

    if amount:
        kwargs["amount"] = amount

    create_order_response = CreateOrder(mode=paypal_mode).create_order(gcp_email, **kwargs)

    response = jsonify({'id': create_order_response.result.id })

    return response, 200, headers
