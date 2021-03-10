import argparse

from app import app

parser = argparse.ArgumentParser(description='Start web trap application.')
parser.add_argument("--port", help="Listening port.", required=True)
args = parser.parse_args()

if __name__ == '__main__':
    app.run(port=args.port, debug=True)
