from setuptools import setup

VERSION = __import__('globomap_api').VERSION

setup(
    name='globomap-api',
    version=VERSION,
    description='Globo globimap-api',
    author='Ederson Brilhante',
    author_email='ederson.brilhante@corp.globo.com',
    install_requires=[
        'Flask==0.12.2',
        'flask-cors==3.0.3',
        'json-spec==0.10.1',
        'python-arango==3.8.0',
    ],
    url='https://github.com/globocom/globomap-api',
    packages=['globomap_api'],
    package_data={'globomap_api': ['models/*.py', 'v1/*.py', 'specs/*.json']},
)
