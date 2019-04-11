# =============================================================================
#          Desc: 
#        Author: chemf
#         Email: eoyohe@gmail.com
#      HomePage: eoyohe.cn
#       Version: 0.0.1
#    LastChange: 2019-04-08 21:10
#       History: 
# =============================================================================
from flask import request
from flask_login import login_required, current_user
from flask_restful import Resource

from app.forms import NoticeForm
from app.model import NoticeModel
from app.permission import permission_required, Role


class Notices(Resource):
    def get(self):
        # tips 没有分页操作，默认公告不多的情况下
        model = NoticeModel.find_all()
        return dict(code=200, msg='success', data=[_.asdict() for _ in model])

    @permission_required(Role.admin)
    def post(self):
        form = NoticeForm(request.form, meta=dict(csrf=False))
        if form.validate():
            m = NoticeModel.new(**form.form)
            return dict(code=200, msg='success', data=m.asdict())
        else:
            return dict(code=400, msg='failure', data=form.errors)


class Notice(Resource):
    def get(self, nid):
        model = NoticeModel.find_by_id(nid)
        if not model:
            return dict(code=404, msg='not found', data=None)
        else:
            return dict(code=200, msg='success', data=model.asdict())

    @login_required
    def delete(self, nid):
        m = NoticeModel.find_one_by(id=nid, user_id=current_user.id)
        if m:
            NoticeModel.delete(m.id)
            return dict(code=200, msg='success', data=None)
        else:
            return dict(code=404, msg='not found', data=None)

    @login_required
    def put(self, nid):
        comment = NoticeModel.find_one_by(id=nid)
        if comment:
            content = request.form['content']
            m = comment.update(comment.id, user_id=current_user.id, content=content)
            return dict(code=200, msg='success', data=m.asdict())
        else:
            return dict(code=404, msg='not found', data=None)

