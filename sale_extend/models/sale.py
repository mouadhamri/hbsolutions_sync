# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
import time
from odoo.exceptions import UserError, AccessError

class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    is_nd = fields.Boolean('ND')
    nd_journal_id = fields.Many2one("account.journal","Journal ND")

class ResPartner(models.Model):
    _inherit = "res.partner"

    is_vc = fields.Boolean('VC')
    linked_account = fields.Many2one("res.partner", "Compte lié")

    def open_partner_ledger(self):
        linked_account_id = self.search([('linked_account','=',self.id)])
        return {
            'type': 'ir.actions.client',
            'name': _('Partner Ledger'),
            'tag': 'account_report',
            'options': {'partner_ids': (linked_account_id | self).ids},
            'ignore_session': 'both',
            'context': "{'model':'account.partner.ledger'}"
        }

    @api.onchange('is_vc')
    def onchange_is_vc(self):
        if self.is_vc:
            account_id = self.env.user.company_id.vc_account_id
            if account_id:
                self.property_account_receivable_id = account_id


class ResCompany(models.Model):
    _inherit = "res.company"

    vc_account_id = fields.Many2one('account.account','Compte VC')

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    linked_account = fields.Many2one(related="partner_id.linked_account",string="Compte lié")

