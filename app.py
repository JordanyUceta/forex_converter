from flask import Flask, request, render_template, jsonify, session, redirect, abort, flash
from flask_debugtoolbar import DebugToolbarExtension
from forex_python.converter import CurrencyRates

c = CurrencyRates()

app = Flask(__name__)
app.config["SECRET_KEY"] = "USD123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app) 

@app.errorhandler(500)
def server_found(e):   
        return redirect('/converter')

@app.route('/')
def main(): 
    """Sends it to the home page"""

    return render_template("index.html")

@app.route('/converter')
def currency_result(): 
    return render_template('converter-form.html')

@app.route('/posting', methods=['post'])
def posted():
    try:
        from_c = request.form['from']
        to_c = request.form['to']
        amount = request.form['amount']
        amount_int = int(amount)

        result = c.convert(from_c, to_c, amount_int)

        return render_template('result.html', result = result)

    except:

        flash("you put an invalid money code", 'wrong')
        return redirect('/converter')