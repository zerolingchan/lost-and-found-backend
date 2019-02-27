from flask import request, Blueprint,jsonify
from flask_login import login_required, current_user
from app.model.comment import CommentModel
from app.common.http import json_response
from app import db


bp_comment = Blueprint('comment', __name__)


@bp_comment.route('/<int:id>')
@login_required
@json_response
def get(id):
    comment = CommentModel.find_one_by(id=id, user_id=current_user.id)
    if comment:
        return dict(code=200, msg='success', data=comment.asdict())
    else:
        return dict(code=404, msg='not found', data=None)


@bp_comment.route('/all')
@login_required
@json_response
def comments():
    comments = current_user.comment_ids
    return dict(
        code=200,
        msg='success',
        data=[_.asdict() for _ in comments]
    )


@bp_comment.route('/create', methods=['POST'])
@login_required
@json_response
def create():
    content = request.form['content']
    m = CommentModel.new(user_id=current_user.id, content=content)
    return dict(code=200, msg='success', data=m.asdict())


@bp_comment.route('/delete/<int:id>')
@login_required
@json_response
def delete(id):
    m = CommentModel.find_one_by(id=id, user_id=current_user.id)
    if m:
        db.session.delete(m)
        db.session.commit()
        return dict(code=200, msg='success', data=None)
    else:
        return dict(code=404, msg='not found', data=None)
