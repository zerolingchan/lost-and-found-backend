from flask_login import login_required, current_user
from flask_restful import Resource

from app.model import LikeModel, PostModel


class Like(Resource):
    @login_required
    def post(self, pid):
        """点赞"""
        like = LikeModel.find_one_by(post_id=pid, user_id=current_user.id)

        post = PostModel.find_by_id(id=pid)
        if not post:
            return dict(code=404, msg='not found post', data=None)

        if not like:
            like = LikeModel.new(post_id=pid, user_id=current_user.id, status=1)
            response = dict(code=200, msg='success', data=None)
        else:
            if not like.status:
                like.update(status=1)
                response = dict(code=200, msg='success', data=None)
            else:
                response = dict(code=201, msg='liked', data=None)

        print(like.asdict())
        post = post.asdict()
        post['like'] = int(like.status)
        response['data'] = post
        return response

    @login_required
    def delete(self, pid):
        """取消点赞"""
        like = LikeModel.find_one_by(post_id=pid, user_id=current_user.id)

        post = PostModel.find_by_id(id=pid).asdict()

        if not like:
            return dict(code=404, msg='dislike', data=None)
        else:
            like.update(status=0)
            post['like'] = int(like.status)
            return dict(code=200, msg='success', data=post)
