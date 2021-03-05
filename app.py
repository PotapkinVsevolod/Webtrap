from flask import Flask


app = Flask(__name__)


@app.route('/<path:path>', methods=["DELETE", "GET", "PATCH", "POST", "PUT", "TRACE"])
def method(path):
    return 'OK', 200


if __name__ == '__main__':
    app.run(debug=True)
