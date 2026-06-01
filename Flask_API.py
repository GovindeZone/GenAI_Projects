from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify([
        {"name": "Raja"},
        {"name": "Kumar"}
    ])

if __name__ == "__main__":
    app.run()