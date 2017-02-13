#! -*- coding: utf8 -*-

from trytond.pool import *
from trytond.model import fields
from trytond.pyson import Eval
from trytond.pyson import Id
from trytond.pyson import Bool, Eval
from trytond.transaction import Transaction

__all__ = ['Party']
__metaclass__ = PoolMeta

class Party:
    __name__ = 'party.party'

    @classmethod
    def __setup__(cls):
        super(Party, cls).__setup__()

    @classmethod
    def validate(cls, parties):
        pool = Pool()
        company_transaction = Transaction().context.get('company')
        Company = pool.get('company.company')
        for party in parties:
            if party.type_document == '04' and bool(party.vat_number):
                super(Party, cls).validate(parties)

            origin = str(parties)

            def in_group():

                ModelData = pool.get('ir.model.data')
                User = pool.get('res.user')
                Group = pool.get('res.group')
                Module = pool.get('ir.module.module')
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
                companies = Company.search([('id', '=', company_transaction)])
                for company in companies:
                    if company.party == party:
                        cls.raise_user_error('No puede modificar los datos de la empresa')
