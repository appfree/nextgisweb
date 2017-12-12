# -*- coding: utf-8 -*-
from rest_query import BaseParamsParser

OPMAP = {'=': 'eq', '!=': 'ne',
         '>': 'gt', '>=': 'ge',
         '<': 'lt', '<=': 'le'}


class ParamsParser(BaseParamsParser):
    exclude_where = []
