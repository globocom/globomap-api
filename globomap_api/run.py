from os import environ

import app


if __name__ == '__main__':
    app.app.config.from_object('config')
    app.app.run('0.0.0.0', int(environ.get('PORT', '5000')))
