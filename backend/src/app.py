from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/contracts")
def get_contracts():
    contracts = [{"ticker": "AAPL", "contract_type": "Call", "quantity": 1}]
    return jsonify(contracts)

if __name__ == "__main__":
    app.run(debug=True)
    