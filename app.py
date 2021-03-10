from datetime import datetime

from flask import Flask, request


HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

app = Flask(__name__)

if not app.debug:
    import logging
    app.logger = logging.getLogger('WebTrapLogger')
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler = logging.FileHandler("main.log")
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)


class StopAwaiting(Exception):
    pass


@app.errorhandler(StopAwaiting)
def handle_stop_awaiting(error):
    return error.__str__(), 200


def process1(timestamp):
    app.logger.info(f'{timestamp} - Process1 started.')


def process2(timestamp):
    if request.args.get('notawaiting') == '1':
        app.logger.error(f"{timestamp} - Process2 closed awaiting.")
        raise StopAwaiting('Process2 closed awaiting.\n')

    app.logger.info(f"{timestamp} - Process2 started.")


def process3(timestamp):
    app.logger.info(f'{timestamp} - Process3 started.')


@app.route('/api', methods=["GET"])
def query():
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
    log_message = f'{timestamp} - {request.method} - {request.path} - {request.args.to_dict()}'

    if request.args.get('invalid') != '1':
        app.logger.info(log_message)
        process1(timestamp)
        process2(timestamp)
        process3(timestamp)
    else:
        app.logger.error(log_message)

    return 'OK', 200


@app.route('/', methods=HTTP_METHODS)
@app.route('/<path:path>', methods=HTTP_METHODS)
def any_path_any_methods_response(path=None):
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
    app.logger.error(f'{timestamp} - {request.method} - {request.path} - {request.args.to_dict()}')
    return 'OK', 200


if __name__ == '__main__':
    app.run(debug=True)
