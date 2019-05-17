from flask_login import login_required, current_user
from flask_restful import Resource

from app.model import LikeModel


class Like(Resource):
    @login_required
    def post(self, pid):
        """点赞"""
        like = LikeModel.find_one_by(post_id=pid, user_id=current_user.id)
        if not like:
            like = LikeModel.new(post_id=pid, user_id=current_user.id, status=1)
            return dict(code=200, msg='success', data=None)
        else:
            return dict(code=201, msg='liked', data=None)

    @login_required
    def delete(self, pid):
        """取消点赞"""
        like = LikeModel.find_one_by(post_id=pid, user_id=current_user.id)
        if not like:
            return dict(code=404, msg='dislike', data=None)
        else:
            like.update(status=0)
            return dict(code=200, msg='success', data=None)
