from flask import Flask, jsonify
from flask_restful import reqparse
from .endpoints import getConversionRate

app = Flask(__name__)
app.config.from_object('config')

@app.route('/output-value', methods=['POST'],)
def output_value():
    """
        Output value rate
    """
    parser = reqparse.RequestParser()
    parser.add_argument('from_money', type=str)
    parser.add_argument('to_money', type=str)
    parser.add_argument('amount', type=int)
    reqargs = parser.parse_args(strict=True)
    if reqargs.get("from_meney") == reqargs.get("to_meney"):
            return {
                "errors": "You must select different plateform"
            }, 401
    #get plateform_money from name
    return jsonify(getConversionRate(reqargs))
