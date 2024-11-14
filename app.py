from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("API_KEY") 
BASE_URL = "http://api.marketstack.com/v1"

def fetch_market_data(symbol):
    endpoint = f"{BASE_URL}/eod"
    params = {
        'access_key': API_KEY,
        'symbols': symbol,
    }
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get('data', [])
    else:
        print("Error:", response.status_code)
        return []

@app.route("/", methods=["GET", "POST"])
def index():
    market_data = []
    symbol = ""
    if request.method == "POST":
        symbol = request.form["symbol"]
        market_data = fetch_market_data(symbol)
    return render_template("index.html", market_data=market_data, symbol=symbol)

if __name__ == "__main__":
    app.run(debug=True)
