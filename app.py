import logging
import time

from flask import Flask, request


app = Flask(__name__)

log = logging.getLogger('WebTrapLogger')
handler = logging.FileHandler("main.log")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
formatter.converter = time.gmtime
handler.setFormatter(formatter)
log.addHandler(handler)
log.setLevel(logging.INFO)


@app.route('/<path:path>', methods=["DELETE", "GET", "PATCH", "POST", "PUT", "TRACE"])
def query(path):
    log_message = f'{request.method} - {request.path} - {request.args.to_dict()}'
    if request.method == "GET":
        log.info(log_message)
    else:
        log.error(log_message)
    return 'OK', 200


if __name__ == '__main__':
    app.run(debug=True)
