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
from flask_restplus import reqparse

from globomap_api.api.v2.parsers import base

post_coll_parser = reqparse.RequestParser()
post_coll_parser.add_argument(
    'data',
    type=str,
    required=True,
    help='Collection',
    location='json'
)


search_all_parser = base.search_parser.copy()
search_all_parser.add_argument(
    'collections',
    type=str,
    required=True,
    default='',
    help='Collections'
)

search_parser = base.search_parser.copy()

post_document_parser = reqparse.RequestParser()
post_document_parser.add_argument(
    'data',
    type=str,
    required=True,
    help='Document',
    location='json'
)

put_document_parser = reqparse.RequestParser()
put_document_parser.add_argument(
    'data',
    type=str,
    required=True,
    help='Document',
    location='json'
)

patch_document_parser = reqparse.RequestParser()
patch_document_parser.add_argument(
    'data',
    type=str,
    required=True,
    help='Document',
    location='json'
)

clear_document_parser = reqparse.RequestParser()
clear_document_parser.add_argument(
    'data',
    type=str,
    required=True,
    help='Query',
    location='json'
)