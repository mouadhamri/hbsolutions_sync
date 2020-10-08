# -*- coding: utf-8 -*-


from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    second_base_url = fields.Char('Lien de la deuxième base', placeholder='http://localhost:8069')
    admin_user = fields.Char('Login')
    admin_password = fields.Char('Mot de passe')
    db_name = fields.Char('Base de données')


class AccountMove(models.Model):
    _inherit = 'account.move'

    synchro_ref = fields.Char('Reference synchronisé')