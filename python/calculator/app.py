from flask import Flask
from flask import request, make_response

from calculator import CongestionTaxCalculator, Car

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.post('/getTax')
def getTax_post():
    """
    An extremely simplified and insecure POST method handler.
    """
    c = CongestionTaxCalculator()
    tax = c.get_tax(vehicle=Car, dates=request.json['dates'])

    return {
        "tax": tax,
    }
