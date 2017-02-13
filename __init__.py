#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from trytond.pool import Pool
from .company import *
from .party import *
from .user import *

def register():
    Pool.register(
        Company,
        Party,
        User,
        module='nodux_admin_one', type_='model')
