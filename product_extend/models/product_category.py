# -*- coding: utf-8 -*-

from odoo import fields, models, api
import time
from odoo.exceptions import UserError, AccessError


class ProductCategory(models.Model):

    _inherit = "product.category"
    _rec_name = 'name'

    hbs_category = fields.Selection([
        ('desktop', 'Ordinateur Bureau'),
        ('laptop', 'Ordinateur Portable'),
        ('tablette', 'Tablette'),
        ('ram', 'RAM'),
        ('cpu', 'CPU'),
        ('screen', 'Écran'),
        ('hard_disk', 'Disque Dur'),
        ('barebone', 'Barebone'),
        ('laptop_barebone', 'Barebone Ord Portable'),
        ('laptop_battery', 'Batterie Ord Portbale'),
        ('aio', 'AIO'),
        ('desktop_uc','Unité centrale'),
    ], string='Type produit')
    is_parent_category = fields.Boolean(string="Catégorie mère ?")
    quantity_control = fields.Boolean(string="Contrôler la quantité ?")
    code_categ = fields.Char('Code')
    separateur = fields.Char()
    code_sku = fields.Char(compute='get_categ_sku', store=True)

    @api.depends('code_categ', 'parent_id','separateur', 'parent_id.code_categ')
    def get_categ_sku(self):
        print('ggggg', self)
        for rec in self:
            sku_code = ''
            separateur = ''
            if not rec.child_id and rec.separateur:
                separateur = rec.separateur
            parent_id = rec.parent_id
            sku_code = (rec.code_categ or '') + separateur

            while parent_id:
                if  parent_id.code_categ:
                    sku_code = parent_id.code_categ +sku_code
                parent_id = parent_id.parent_id
            rec.code_sku = sku_code




