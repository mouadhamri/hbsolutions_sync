from odoo import models,fields, api, _
from odoo.exceptions import UserError


class ValidateAccountMove(models.TransientModel):
    _name = "change.account.move"
    _description = "Change invoice"

    partner_id = fields.Many2one('res.partner','Client',required=True)
    journal_id = fields.Many2one('account.journal','Journal',readonly=True)
    invoice_id = fields.Many2one('account.move','Facture',readonly=True)
    line_ids = fields.One2many('change.account.move.line','change_move_id','Lignes')

    @api.model
    def default_get(self, fields):
        res = super(ValidateAccountMove, self).default_get(fields)
        context = dict(self._context or {})
        moves = self.env['account.move'].browse(context.get('active_ids'))
        moves_ko = moves.filtered(lambda r: r.type not in ('out_invoice', 'out_refund'))
        if len(moves_ko):
            raise UserError(_('Vous pouvez choisir seulement des factures / avoirs client.'))
        if len(moves) > 1:
            raise UserError(_("Vous ne pouvez pas traiter plus qu'un document à la fois!"))
        #lines = self.env['change.account.move.line']
        #for line in moves.invoice_line_ids:
            #lines |= self.env['change.account.move.line'].create({
                #'name': line.name,
                #'product_id': line.product_id.id,
                #'price_unit': line.price_unit,
                #'qty': line.quantity,
                #'tax_ids': [(6, 0, line.tax_ids.ids)],
                #'account_move_line_id':line.id,
            #})
        res.update({
            #'line_ids': lines.ids,
            'journal_id': moves.journal_id.id,
            'invoice_id':moves.id,
        })
        return res

    def change_move(self):
        for rec in self:
            # invoice_id = rec.invoice_id.copy({'partner_id': rec.partner_id.id})
            # invoice_id.line_ids.unlink()
            # inv_line_ids = []
            # for line in rec.line_ids:
            #     if line.qty > 0 and line.price_unit > 0:
            #         inv_line_ids.append((0, 0, {
            #             'name': line.account_move_line_id.name,
            #             'account_id': line.account_move_line_id.account_id,
            #             'price_unit': line.price_unit,
            #             'quantity': line.qty,
            #             'product_id': line.account_move_line_id.product_id.id,
            #             'product_uom_id': line.account_move_line_id.product_uom_id.id,
            #             'tax_ids': [(6, 0, line.account_move_line_id.tax_ids.ids)],
            #             'analytic_tag_ids': [(6, 0, line.account_move_line_id.analytic_tag_ids.ids)],
            #             'analytic_account_id': line.account_move_line_id.analytic_account_id,
            #         }))
            #         line.account_move_line_id.write({
            #             'quantity':line.account_move_line_id.quantity - line.qty,
            #         })
            rec.invoice_id.write({'partner_id':rec.partner_id})
            for line in rec.invoice_id.line_ids:
                if line.partner_id:
                    line.write({'partner_id':rec.partner_id})
        return {'type': 'ir.actions.act_window_close'}

class ValidateAccountMoveLine(models.TransientModel):
    _name = "change.account.move.line"
    _description = "Change invoice line"

    change_move_id = fields.Many2one('change.account.move', string='Change invoice',readonly=True)
    product_id = fields.Many2one('product.product', string='Article',readonly=True)
    name = fields.Char('Description',readonly=True)
    price_unit = fields.Float(string='Prix unitaire',readonly=True)
    qty = fields.Float(string='Quantité')
    tax_ids = fields.Many2many('account.tax', string='Tva',readonly=True)
    account_move_line_id = fields.Many2one('account.move.line', string='Ligne facture',readonly=True)

    @api.onchange('price_unit','qty')
    def onchange_price_unit(self):
        if self.price_unit > self.account_move_line_id.price_unit:
            raise UserError(_("Le prix ne doit pas dépasser le prix de la ligne!"))
        if self.qty > self.account_move_line_id.quantity:
            raise UserError(_("Le quantité ne doit pas dépasser la quantité de la ligne!"))
