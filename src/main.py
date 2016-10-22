import sys

import app


if __name__ == '__main__':
    application = app.create_app()
    try:
        port = sys.argv[1]
    except IndexError:
        port = 5000
    application.run(debug=True, host='127.0.0.1')