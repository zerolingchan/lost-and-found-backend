# =============================================================================
#          Desc: 
#        Author: chemf
#         Email: eoyohe@gmail.com
#      HomePage: eoyohe.cn
#       Version: 0.0.1
#    LastChange: 2019-04-08 21:10
#       History: 
# =============================================================================
from flask import request, abort
from flask_restful import Resource

from app.model import NoticeModel
from app.permission import permission_required, Role
from app.forms import NoticeForm


class Notices(Resource):
    def get(self):
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

