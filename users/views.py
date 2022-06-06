from werkzeug.exceptions import BadRequest

from . import bp
from .models import User


@bp.route('/users', methods=['get', 'post'])
def users():
    User.query.all()
    raise BadRequest('Invalid user')
