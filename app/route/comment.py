from flask import request, Blueprint
from flask_login import current_user, login_required
from flask_restful import Resource

from app import db
from app.forms import PaginationForm
from app.model.comment import CommentModel


class Comments(Resource):
    def get(self):
        """
        获得所有留言
        :return:
        """
        paginate_form = PaginationForm(request.values)
        pagination = CommentModel.query.paginate(**paginate_form.form)

        return dict(
            code=200,
            msg='success',
            data=dict(
                data=[_.asdict() for _ in pagination.items],
                current_page=pagination.page,
                current_num=len(pagination.items),
                total_page=pagination.pages,
                total_num=pagination.total
            )
        )

    @login_required
    def post(self):
        content = request.form['content']
        m = CommentModel.new(user_id=current_user.id, content=content)
        return dict(code=200, msg='success', data=m.asdict())


class Comment(Resource):
    def get(self, cid):
        comment = CommentModel.find_one_by(id=cid)
        if comment:
            return dict(code=200, msg='success', data=comment.asdict())
        else:
            return dict(code=404, msg='not found', data=None)

    @login_required
    def delete(self, cid):
        m = CommentModel.find_one_by(id=cid, user_id=current_user.id)
        if m:
            db.session.delete(m)
            db.session.commit()
            return dict(code=200, msg='success', data=None)
        else:
            return dict(code=404, msg='not found', data=None)

    @login_required
    def put(self, cid):
        comment = CommentModel.find_one_by(id=cid, user_id=current_user.id)
        if comment:
            content = request.form['content']
            m = comment.update(content=content)
            return dict(code=200, msg='success', data=comment.asdict())
        else:
            return dict(code=404, msg='not found', data=None)

