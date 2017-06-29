from os import environ
from api.app import create_app


application = create_app('config')

if __name__ == '__main__':
    application.run('0.0.0.0', int(environ.get('PORT', '5000')))
