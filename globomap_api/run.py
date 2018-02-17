# -*- coding: utf-8 -*-
"""
   Copyright 2018 Globo.com

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from logging import config
from os import environ

from app import create_app
from config import LOGGING

if __name__ == '__main__':
    config.dictConfig(LOGGING)
    application = create_app()
    application.run(
        '0.0.0.0',
        int(environ.get('PORT', '5000')),
        debug=True,
        threaded=True
    )
