from flask import jsonify

from . import bp
from .models import User


@bp.get('/users')
def users():
    user_list = User.query.all()
    return jsonify([item.to_dict() for item in user_list])
