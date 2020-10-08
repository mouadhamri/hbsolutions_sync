# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    is_nd = fields.Boolean('ND')