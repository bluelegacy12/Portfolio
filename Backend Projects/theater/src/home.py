from flask import Blueprint, render_template
from .models import db, Performers, Roles, Shows, Conflicts, Scenes, performers_conflicts, scenes_roles

bp = Blueprint('index', __name__, url_prefix='/')

@bp.route('', methods=['GET'])
def index():
    context = {}
    context['performers'] = Performers.query.all()
    return render_template('home.html', context=context)




