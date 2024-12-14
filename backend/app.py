from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    server_name = os.getenv("SERVER_NAME", "unknown")
    return jsonify({"message": f"Hello from {server_name}!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
