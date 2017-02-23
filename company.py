#! -*- coding: utf8 -*-
from trytond.pool import *
from trytond.model import fields
from trytond.pyson import Eval
from trytond.pyson import Id
from trytond.pyson import Bool, Eval
from trytond.transaction import Transaction

__all__ = ['Company']
__metaclass__ = PoolMeta

class Company:
    __name__ = 'company.company'

    permission = fields.Function(fields.Char('Permission'), 'get_permission')

    @classmethod
    def __setup__(cls):
        super(Company, cls).__setup__()
        cls.party.states['readonly'] = Eval('permission') == 'False'

    @classmethod
    def get_permission(cls, companies, names):
        pool = Pool()
        origin = str(companies)

        def in_group():
            pool = Pool()
            ModelData = pool.get('ir.model.data')
            User = pool.get('res.user')
            Group = pool.get('res.group')
            Module = pool.get('ir.module')
            group = Group(ModelData.get_id('nodux_admin_one',
                            'group_change_company'))
            transaction = Transaction()
            user_id = transaction.user
            if user_id == 0:
                user_id = transaction.context.get('user', user_id)
            if user_id == 0:
                return True
            user = User(user_id)
            return origin and group in user.groups

        result = {n: {s.id: 'False' for s in companies} for n in names}
        for name in names:
            for company in companies:
                if not in_group():
                    result[name][company.id] = 'False'
                else:
                    result[name][company.id] = 'True'
        return result

    @classmethod
    def validate(cls, companies):
        for company in companies:
            origin = str(companies)

            def in_group():
                pool = Pool()
                ModelData = pool.get('ir.model.data')
                User = pool.get('res.user')
                Group = pool.get('res.group')
                Module = pool.get('ir.module')
                group = Group(ModelData.get_id('nodux_admin_one',
                                'group_system_admin'))
                transaction = Transaction()
                user_id = transaction.user
                if user_id == 0:
                    user_id = transaction.context.get('user', user_id)
                if user_id == 0:
                    return True
                user = User(user_id)
                return origin and group in user.groups

            if not in_group():
                cls.raise_user_error('No puede modificar los datos de la empresa')
