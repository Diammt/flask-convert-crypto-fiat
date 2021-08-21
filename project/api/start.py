from flask import Flask, jsonify, abort
from flask_restful import reqparse
from .endpoints import getConversionRate
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.config.from_object('config')

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Fiat-conversion"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

@app.route('/convert', methods=['POST'],)
def output_value():
    """
        Make conversion
        ---
        tags:
          - make-conversion
        parameters:
          - in: body
            name: body
            schema:
              required:
                - from
                - to
                - amount
              properties:
                from:
                  type: string
                  example: BTC
                  description: fiat origin source name
                to:
                  type: string
                  example: USD
                  description: fiat destination name
                amount:
                  type: string
                  example: 1
                  description: fiat origin amount
        responses:
          201:
            description: Output value
    """
    parser = reqparse.RequestParser()
    parser.add_argument('from', type=str)
    parser.add_argument('to', type=str)
    parser.add_argument('amount', type=int)
    reqargs = parser.parse_args(strict=True)
    if reqargs.get("from") == reqargs.get("to"):
            return {
                "errors": "You must select different plateform"
            }, 401
    #get plateform_money from name
    return jsonify(getConversionRate(reqargs))
