# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ProductProduct(models.Model):
    _inherit = 'product.product'


    synch_id = fields.Integer(u'Id synchronisation')


class ProductCategory(models.Model):
    _inherit = 'product.category'


    synch_id = fields.Integer(u'Id synchronisation')


class ResPartner(models.Model):
    _inherit = 'res.partner'


    synch_id = fields.Integer('Id synchronisation')


class AccountMove(models.Model):
    _inherit = 'account.move'

    synch_id = fields.Integer('Id synchronisation')
    nd_move = fields.Boolean('ND')

    def remote_action_post(self):
        self.action_post()
        return True

    def action_nd_ok(self):
        for rec in self:
            if rec.nd_move:
                rec.nd_move = False

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    synch_id = fields.Integer('Id synchronisation')


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    synch_id = fields.Integer('Id synchronisation')


class ResBank(models.Model):
    _inherit = 'res.bank'

    synch_id = fields.Integer('Id synchronisation')




