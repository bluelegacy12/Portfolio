from flask import Blueprint, jsonify, abort, request
from ..models import db, Performers, Roles, Shows, Conflicts, Scenes, performers_conflicts, scenes_roles

bp = Blueprint('performers', __name__, url_prefix='/performers')

@bp.route('', methods=['GET'])
def index_performers():
    performers = Performers.query.all()
    result = []
    for p in performers:
        result.append(p.serialize())
    return jsonify(result)


@bp.route('/<int:id>', methods=['GET'])
def show_performer(id: int):
    p = Performers.query.get_or404(id)
    return jsonify(p.serialize())


@bp.route('', methods=['POST'])
def create_performer():
    if 'name' not in request.json or 'phone' not in request.json or 'email' not in request.json:
        return abort(400)

    p = Performers(
        name=request.json['name'],
        phone=request.json['phone'],
        email=request.json['email']
    )
    db.session.add(p)
    db.session.commit()
    return jsonify(p.serialize())


@bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update_performer(id: int):
    p = Performers.query.get_or_404(id)
    if 'name' in request.json:
        p.name = request.json['name']
    if 'phone' in request.json:
        p.phone = request.json['phone']
    if 'email' in request.json:
        p.email = request.json['email']
    try:
        db.session.commit()
        return jsonify(p.serialize())
    except:
        return jsonify(False)


@bp.route('/<int:id>', methods=['DELETE'])
def delete_performer(id: int):
    p = Performers.query.get_or_404(id)
    try:
        db.session.delete(p)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)


@bp.route('', methods=['POST'])
def add_show():
    if 'title' not in request.json or 'rehearsal_start' not in request.json or 'show_open' not in request.json or 'director_id' not in request.json:
        return abort(400)
    s = Shows(
        title=request.json['title'],
        rehearsal_start=request.json['rehearsal_start'],
        show_open=request.json['show_open'],
        director_id=request.json['director_id']
    )
    db.session.add(s)
    db.session.commit()
    return jsonify(s.serialize())


@bp.route('/<int:id>', methods=['POST'])
def add_role(id: int):
    if 'role' not in request.json or 'show' not in request.json:
        return abort(400)
    p = Performers.query.get_or_404(id)


@bp.route('/<int:id>', methods=['GET'])
def performer_roles(id: int):
    p = Performers.query.get_or_404(id)
    r = Roles.query.get_or_404(id)
    result = []
    for role in r.performer_id:
        if role == id:
            result.append(r.name.serialize())
    return jsonify(result)
