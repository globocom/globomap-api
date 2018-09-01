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
import math

from flask import current_app as app

from globomap_api import util


def search(name, data, page, per_page):
    """Search in Database"""

    spec = app.config['SPECS'].get('search')
    util.json_validate(spec).validate(data)

    db_inst = app.config['ARANGO_CONN']

    db_inst.get_database()
    cursor = db_inst.search_in_collection(name, data, page, per_page)

    total_pages = int(math.ceil(cursor.statistics()[
                      'fullCount'] / (per_page * 1.0)))
    total_documents = cursor.statistics()['fullCount']

    docs = [doc for doc in cursor]

    res = {
        'total_pages': total_pages,
        'total': len(docs),
        'total_documents': total_documents,
        'documents': docs
    }

    return res
