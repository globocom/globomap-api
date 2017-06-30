from flask import Blueprint


api = Blueprint('api', __name__)


# do this last to avoid circular dependencies
from . import vips
