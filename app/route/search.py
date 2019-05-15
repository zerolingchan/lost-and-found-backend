from flask_restful import Resource
from sqlalchemy import or_
from collections import defaultdict

from app.forms import SearchForm
from app.util import json_response
from app.model import PostModel


class Search(Resource):
    def post(self):
        form = SearchForm(meta=dict(csrf=False))
        if form.validate():
            word = form.word.data
            query = PostModel.get_query()\
                .filter(or_(PostModel.content.like(f'%{word}%'),
                             PostModel.title.like(f'%{word}%')))
            data = defaultdict(list)
            for p in query.all():
                data[p.type].append(p.asdict())
            return dict(code=200, msg='success', data=data)
        else:
            return dict(code=400, msg='params error', data=form.errors)
