# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):

    _inherit = "product.template"

    hbs_category = fields.Selection(string="Type produit", related="categ_id.hbs_category", store=True)
    test1 = fields.Char(string="test1")
    test2 = fields.Char(string="test2")
    maker = fields.Many2one("hbs.maker", string="Fabricant")
    grade = fields.Many2one("hbs.grade", string="Grade")
    model = fields.Many2one("hbs.model", string="Modèle")
    cpu = fields.Many2one("hbs.cpu", string="CPU")
    cpu_core_number = fields.Many2one("hbs.core.number", string="Nombre de core")
    cpu_state = fields.Selection([
        ('new', 'Neuf'),
        ('occasion', 'Occasion')
    ], default='new', string="État")
    screen_resolution = fields.Many2one("hbs.screen.resolution", string="Résolution")
    screen_size = fields.Many2one("hbs.screen.size", string="Taille")
    screen_raye = fields.Boolean('Rayé')
    screen_tache = fields.Boolean('Taché')
    screen_casse = fields.Boolean('Cassé')
    product_state = fields.Selection([
        ('ok', 'OK'),
        ('hs', 'HS'),
    ], default='ok', string="État")
    ram_technology = fields.Many2one("hbs.ram.technology", string="Technologie")
    #ram_number = fields.Integer(string="Nombre de barrette", default=1)
    ram_number = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
    ], string='Nombre de barrette', default='1')
    ram_size1 = fields.Many2one("hbs.ram.size", string="Taille RAM 1")
    ram_size2 = fields.Many2one("hbs.ram.size", string="Taille RAM 2")
    ram_size3 = fields.Many2one("hbs.ram.size", string="Taille RAM 3")
    ram_size4 = fields.Many2one("hbs.ram.size", string="Taille RAM 4")
    ram_size5 = fields.Many2one("hbs.ram.size", string="Taille RAM 5")
    ram_size6 = fields.Many2one("hbs.ram.size", string="Taille RAM 6")
    ram_size7 = fields.Many2one("hbs.ram.size", string="Taille RAM 7")
    ram_size8 = fields.Many2one("hbs.ram.size", string="Taille RAM 8")
    total_ram = fields.Integer("Total ram",compute="get_total_ram")
    ram_state = fields.Selection([
        ('new', 'Neuf'),
        ('occasion', 'Occasion')
    ], default='new', string="État")
    ram_form_factor = fields.Many2one("hbs.form.factor", string="Facteur de forme")
    #hard disk 1
    hard_disk_technology = fields.Many2one("hbs.hard.disk.technology", string="Technologie")
    hard_disk_size = fields.Many2one("hbs.hard.disk.size", string="Taille")
    hard_disk_state = fields.Selection([
        ('new', 'Neuf'),
        ('occasion', 'Occasion'),
        ('refurbished', 'Reconditionné'),
    ], default='new', string="État")

    # hard disk 2
    hard_disk_technology_2 = fields.Many2one("hbs.hard.disk.technology", string="Technologie")
    hard_disk_size_2 = fields.Many2one("hbs.hard.disk.size", string="Taille")
    hard_disk_state_2 = fields.Selection([
        ('new', 'Neuf'),
        ('occasion', 'Occasion'),
        ('refurbished', 'Reconditionné'),
    ], default='new', string="État")

    graphic_card_technology = fields.Many2one("hbs.graphic.card.technology", string="Nom")
    graphic_card_size = fields.Many2one("hbs.graphic.card.size", string="Taille")
    keyboard = fields.Many2one("hbs.keyboard", string="Clavier")
    camera = fields.Boolean(string="Avec caméra")
    battery = fields.Boolean(string="Avec batterie")
    support = fields.Boolean(string="Avec support")
    lecteur = fields.Boolean(string="Avec lecteur")
    battery_state = fields.Selection([
        ('new', 'Neuf'),
        ('occasion', 'Occasion')
    ], default='new', string="État")
    charger = fields.Boolean(string="Avec chargeur")
    wide = fields.Boolean(string="Wide")
    hdmi = fields.Boolean(string="HDMI")
    cost_currency_id = fields.Integer("iii")
    nbr_bom = fields.Integer('Nbr NC', compute="_get_nbr_bom", store=True)
    default_code_long = fields.Char()
    barcode_long = fields.Char()
    screen_connectique = fields.Many2one('hbs.screen.connectique', 'Connectique')
    screen_format = fields.Many2one('hbs.screen.format', 'Format')
    aio_text = fields.Text('Autre information')

    #BOM products
    screen_product = fields.Many2one('product.product','Ecran (article)')
    model_product = fields.Many2one('product.product','Modèle (article)')
    cpu_product = fields.Many2one('product.product','CPU (article)')
    ram_product_1 = fields.Many2one('product.product','RAM 1 (article)')
    ram_product_2 = fields.Many2one('product.product','RAM 2 (article)')
    ram_product_3 = fields.Many2one('product.product','RAM 3 (article)')
    ram_product_4 = fields.Many2one('product.product','RAM 4 (article)')
    ram_product_5 = fields.Many2one('product.product','RAM 5 (article)')
    ram_product_6 = fields.Many2one('product.product','RAM 6 (article)')
    ram_product_7 = fields.Many2one('product.product','RAM 7 (article)')
    ram_product_8 = fields.Many2one('product.product','RAM 8 (article)')
    disk_product_1 = fields.Many2one('product.product','Disque dur 1 (article)')
    disk_product_2 = fields.Many2one('product.product','Disque dur 2 (article)')
    graphic_card_product = fields.Many2one('product.product','Carte graphique (article)')
    keyboard_product = fields.Many2one('product.product','Clavier (article)')
    battery_product = fields.Many2one('product.product','Batterie (article)')
    charger_product = fields.Many2one('product.product','Chargeur (article)')
    ref_variante = fields.Char("Ref constructeur", compute="_get_ref")

    @api.depends('variant_seller_ids', 'variant_seller_ids.product_code')
    def _get_ref(self):
        for rec in self:
            rec.ref_variante = ""
            if rec.variant_seller_ids:
                sellers = rec.variant_seller_ids.filtered(lambda r: r.product_code and r.product_tmpl_id == rec).sorted(
                    key=lambda r: str(r.create_date), reverse=True)
                if sellers:
                    s_price = sellers[0]
                    for s in sellers:
                        if s.product_id == rec:
                            s_price = s
                            break
                    for s in sellers:
                        if s.create_date:
                            s_price = s
                            break
                    rec.ref_variante = s_price.product_code

    def get_total_ram(self):
        for rec in self:
            rec.total_ram = int(rec.ram_size1.name)+int(rec.ram_size2.name)+int(rec.ram_size3.name)+int(rec.ram_size4.name)+int(rec.ram_size5.name)+int(rec.ram_size6.name)+int(rec.ram_size7.name)+int(rec.ram_size8.name)

    @api.depends('bom_ids')
    def _get_nbr_bom(self):
        self.nbr_bom = len(self.bom_ids)

    _sql_constraints = [

        ('unique_default_code_long', 'UNIQUE(default_code_long)',
         'ce code SKU existe déja'),

    ]

    @api.onchange('maker', 'grade', 'model', 'cpu', 'screen_resolution',
                  'screen_size', 'keyboard', 'camera', 'categ_id', 'ram_number',
                  'ram_technology', 'ram_size1', 'ram_size2', 'ram_size3', 'ram_size4',
                  'ram_size5', 'ram_size6', 'ram_size7', 'ram_size8', 'hard_disk_technology',
                  'hard_disk_size','hard_disk_technology_2','hard_disk_size_2', 'graphic_card_technology', 'battery',
                  'charger', 'ram_state', 'ram_form_factor', 'cpu_state', 'cpu_core_number',
                  'product_state', 'wide', 'battery_state', 'hard_disk_state', 'screen_connectique', 'screen_format'
                  )
    def onchange_product_details_hbs(self):
        default_code = ""
        name = ""
        description = ""
        if self.model:
            self.screen_size = False
            self.ram_technology = False
            if self.model.screen_size:
                self.screen_size = self.model.screen_size.id
            if self.model.ram_technology:
                self.ram_technology = self.model.ram_technology.id
        # product category
        if self.hbs_category in ("ram", "desktop"):
            if self.ram_form_factor:
                default_code += self.ram_form_factor.code
        if self.hbs_category:
            if self.hbs_category == "tablette":
                default_code += "TBL"
                description += "Tablette"
            elif self.hbs_category == "laptop":
                default_code += "LPT"
                description += "PC Portable"
            elif self.hbs_category == "desktop":
                description += "PC de Bureau"
            elif self.hbs_category == "aio":
                default_code += "AIO"
                description += "AIO"
            elif self.hbs_category == "laptop_barebone":
                default_code += "LPT"
                description += "PC Portable Barebone"
                name += "PC Portable Barebone"
            elif self.hbs_category == "ram":
                default_code += "RAM"
                description += "Carte RAM"
                name += "Carte RAM"
                if self.ram_state:
                    if self.ram_state == "new":
                        default_code += "N"
                    else:
                        default_code += "D"
            elif self.hbs_category == "laptop_battery":
                default_code += "BTL"
                description += "Batterie de PC Portable"
                if self.battery_state:
                    if self.battery_state == "new":
                        default_code += "N"
                    else:
                        default_code += "D"
            elif self.hbs_category == "cpu":
                default_code += "CPU"
                description += "Processeur"
                if self.cpu_state:
                    if self.cpu_state == "new":
                        default_code += "N"
                    else:
                        default_code += "D"
            elif self.hbs_category == "screen":
                default_code += "DSP"
                description += "Ecran"
                if self.product_state:
                    default_code += self.product_state.upper()
            elif self.hbs_category == "hard_disk":
                default_code += "DRV"
                name += "Disque dur"
                if self.hard_disk_state:
                    if self.hard_disk_state == "new":
                        default_code += "N"
                    elif self.hard_disk_state == "occasion":
                        default_code += "D"
                    else:
                        default_code += "R"
            if self.grade:
                default_code += self.grade.code
            if self.maker:
                default_code += self.maker.code
                name += " " + self.maker.name
                description += " " + self.maker.name
            if self.hbs_category == "hard_disk":
                default_code += "-"
            if self.model:
                default_code += "-" + self.model.code
                name += " " + self.model.name
                description += " " + self.model.name
            if self.hbs_category in ("ram", "desktop"):
                if self.ram_form_factor:
                    name += " " + self.ram_form_factor.name
                    description += " " + self.ram_form_factor.name
            if self.screen_size:
                name += " " + self.screen_size.code + '" '
                description += " " + self.screen_size.code + '" '
            if self.screen_resolution:
                if self.hbs_category == "screen" and self.screen_size:
                    default_code += "-" + self.screen_size.code
                default_code += self.screen_resolution.code
                name += self.screen_resolution.name
                description += self.screen_resolution.name
            if self.cpu:
                default_code += "-" + self.cpu.code
                name += " " + self.cpu.name_code
                description += " " + self.cpu.name

            if self.hbs_category not in ['laptop_barebone', 'screen']:
                print('aze')
                if self.ram_number:

                    size = 0
                    if (int(self.ram_number) >= 1):
                        size += int(self.ram_size1.name)
                    if (int(self.ram_number) >= 2):
                        size += int(self.ram_size2.name)
                    if (int(self.ram_number) >= 3):
                        size += int(self.ram_size3.name)
                    if (int(self.ram_number) >= 4):
                        size += int(self.ram_size4.name)
                    if (int(self.ram_number) >= 5):
                        size += int(self.ram_size5.name)
                    if (int(self.ram_number) >= 6):
                        size += int(self.ram_size6.name)
                    if (int(self.ram_number) >= 7):
                        size += int(self.ram_size7.name)
                    if (int(self.ram_number) >= 8):
                        size += int(self.ram_size8.name)
                    if size != 0:
                        default_code += "-" + str(size).zfill(2)
                        name += " " + str(size) + "GB"
                        description += " " + str(size) + "GB"
                if self.ram_technology:

                    default_code += self.ram_technology.code
                    description += " " + self.ram_technology.name
                if self.hard_disk_size:
                    default_code += self.hard_disk_size.code
                    name += " " + self.hard_disk_size.code + "GB"
                    description += " " + self.hard_disk_size.code + "GB"
                if self.hard_disk_technology:
                    default_code += self.hard_disk_technology.code
                    description += " " + self.hard_disk_technology.name
                    if self.hbs_category == "hard_disk":
                        name += " " + self.hard_disk_technology.name

                if self.hard_disk_size_2:
                    default_code += self.hard_disk_size_2.code
                    name += " " + self.hard_disk_size_2.code + "GB"
                    description += " " + self.hard_disk_size_2.code + "GB"
                if self.hard_disk_technology_2:
                    default_code += self.hard_disk_technology_2.code
                    description += " " + self.hard_disk_technology_2.name
                    if self.hbs_category == "hard_disk":
                        name += " " + self.hard_disk_technology_2.name

            print("ok")
            print(default_code)
            if self.keyboard:
                default_code += "-" + self.keyboard.code
                description += " " + self.keyboard.name
            if self.camera:
                default_code += "W"
                description += " Webcam"
            if self.hbs_category == "cpu":
                if self.cpu_core_number:
                    default_code += self.cpu_core_number.code
                    name += " " + self.cpu_core_number.name
                    description += " " + self.cpu_core_number.name
            if self.screen_format:
                default_code += self.screen_format.code
                name += " " +self.screen_format.name
                description += " " +self.screen_format.name
            if self.screen_connectique:
                default_code += self.screen_connectique.code
                name += " " +self.screen_connectique.name
                description += " " +self.screen_connectique.name
            if self.graphic_card_technology:
                default_code += self.graphic_card_technology.code
                description += " " + self.graphic_card_technology.name
                name += " " + self.graphic_card_technology.name
            if self.hbs_category == 'screen' and self.model:
                if '-' in default_code:
                    default_code = default_code.split('-')[0]
                default_code += '-'+self.model.code
                name = "Ecran"
                if self.maker:
                    name += " "+self.maker.name + '-'+self.model.code
                description = name

        self.default_code_long = default_code.strip()
        self.barcode_long = default_code.strip()
        self.name = name.strip()
        self.description = description.strip()
        self.description_pickingout = description.strip()
        self.description_picking = description.strip()


    def generate_default_code(self):
        for rec in self:
            if not rec.categ_id or not rec.categ_id.code_sku:
                raise ValidationError('Merci de définir la catégorie et le code de la catégorie!')
            else:
                code_sku = rec.categ_id.code_sku
                if rec.maker:
                    code_sku += rec.maker.name
                seq = self.env['product.default.code'].search([('name', '=', rec.default_code_long.strip())])
                if seq:
                    code_sku = code_sku + seq[0].sequence
                else:
                    seq = self.env['product.default.code'].create({'name': rec.default_code_long.strip()})
                    code_sku = code_sku + seq[0].sequence

                rec.default_code = code_sku
                rec.barcode = code_sku

    def create_bom_line(self,bom_id,product_id):
        if product_id and bom_id:
            self.env['mrp.bom.line'].create({
                'bom_id': bom_id.id,
                'product_id': product_id.id,
                'product_qty': 1.0,
            })

    def mrp_bom_generate(self):
        self.ensure_one()
        if not self.bom_ids:
            bom_id = self.env['mrp.bom'].create({
                'product_tmpl_id': self.id,
                'code': self.default_code_long,
                'product_qty': 1.0,
                'type': 'normal',
            })
            self.create_bom_line(bom_id,self.screen_product)
            self.create_bom_line(bom_id,self.model_product)
            self.create_bom_line(bom_id,self.cpu_product)
            self.create_bom_line(bom_id,self.ram_product_1)
            self.create_bom_line(bom_id,self.ram_product_2)
            self.create_bom_line(bom_id,self.ram_product_3)
            self.create_bom_line(bom_id,self.ram_product_4)
            self.create_bom_line(bom_id,self.ram_product_5)
            self.create_bom_line(bom_id,self.ram_product_6)
            self.create_bom_line(bom_id,self.ram_product_7)
            self.create_bom_line(bom_id,self.ram_product_8)
            self.create_bom_line(bom_id,self.disk_product_1)
            self.create_bom_line(bom_id,self.disk_product_2)
            self.create_bom_line(bom_id,self.graphic_card_product)
            self.create_bom_line(bom_id,self.keyboard_product)
            self.create_bom_line(bom_id,self.battery_product)
            self.create_bom_line(bom_id,self.charger_product)
        else:
            raise ValidationError("Une nomenclature est déjà créée!")


    def get_sku_name_description_by_category(self, category):
        default_code = ""
        name = ""
        description = ""
        if self.model:
            self.screen_size = False
            self.ram_technology = False
            if self.model.screen_size:
                self.screen_size = self.model.screen_size.id
            if self.model.ram_technology:
                self.ram_technology = self.model.ram_technology.id
        # product category
        if category in ("ram", "desktop"):
            if self.ram_form_factor:
                default_code += self.ram_form_factor.code
        if category:
            if category == "laptop_barebone":
                default_code += "LPT"
                description += "PC Portable Barebone"
            elif category == "ram":
                default_code += "RAM"
                description += "Carte RAM"
                if self.ram_state:
                    if self.ram_state == "new":
                        default_code += "N"
                    else:
                        default_code += "D"
            elif category == "cpu":
                default_code += "CPU"
                description += "Processeur"
                if self.cpu_state:
                    if self.cpu_state == "new":
                        default_code += "N"
                    else:
                        default_code += "D"
            elif category == "hard_disk":
                default_code += "DRV"
                if self.hard_disk_state:
                    if self.hard_disk_state == "new":
                        default_code += "N"
                    elif self.hard_disk_state == "occasion":
                        default_code += "D"
                    else:
                        default_code += "R"
            if category in ("laptop_barebone", "desktop"):
                if self.grade:
                    default_code += self.grade.code
            if category in ("laptop_barebone", "hard_disk"):
                if self.maker:
                    default_code += self.maker.code
                    name += " " + self.maker.name
                    description += " " + self.maker.name
            if category == "hard_disk":
                default_code += "-"
            if self.model:
                default_code += "-" + self.model.code
                name += " " + self.model.name
                description += " " + self.model.name
            if category in ("ram", "desktop"):
                if self.ram_form_factor:
                    name += " " + self.ram_form_factor.name
                    description += " " + self.ram_form_factor.name
            if category in ("laptop_barebone"):
                if self.screen_resolution:
                    if category == "screen":
                        default_code += "-" + self.screen_size.code
                    default_code += self.screen_resolution.code
                    name += self.screen_resolution.name
                    description += self.screen_resolution.name
            if category in ["laptop_barebone", "cpu"]:
                if self.cpu:
                    default_code += "-" + self.cpu.code
                    name += " " + self.cpu.name_code
                    description += " " + self.cpu.name
            if category not in ['laptop_barebone', 'cpu', 'hard_disk']:
                if self.ram_number  and self.hbs_category != 'screen':

                    size = 0
                    if (int(self.ram_number) >= 1):
                        size += int(self.ram_size1.name)
                    if (int(self.ram_number) >= 2):
                        size += int(self.ram_size2.name)
                    if (int(self.ram_number) >= 3):
                        size += int(self.ram_size3.name)
                    if (int(self.ram_number) >= 4):
                        size += int(self.ram_size4.name)
                    if (int(self.ram_number) >= 5):
                        size += int(self.ram_size5.name)
                    if (int(self.ram_number) >= 6):
                        size += int(self.ram_size6.name)
                    if (int(self.ram_number) >= 7):
                        size += int(self.ram_size7.name)
                    if (int(self.ram_number) >= 8):
                        size += int(self.ram_size8.name)
                    if size != 0:
                        default_code += "-" + str(size).zfill(2)
                        name += " " + str(size) + "GB"
                        description += " " + str(size) + "GB"
                if self.ram_technology:
                    default_code += self.ram_technology.code
                    description += " " + self.ram_technology.name
                if self.hard_disk_size:
                    default_code += self.hard_disk_size.code
                    name += " " + self.hard_disk_size.code + "GB"
                    description += " " + self.hard_disk_size.code + "GB"
                if self.hard_disk_technology:
                    default_code += self.hard_disk_technology.code
                    description += " " + self.hard_disk_technology.name
                    if category == "hard_disk":
                        name += " " + self.hard_disk_technology.name
                if self.keyboard:
                    default_code += self.keyboard.code
                    description += " " + self.keyboard.name
                if self.camera:
                    default_code += "W"
                    description += " Webcam"
                if category == "cpu":
                    if self.cpu_core_number:
                        default_code += self.cpu_core_number.code
                        name += " " + self.cpu_core_number.name
                        description += " " + self.cpu_core_number.name
                if self.screen_format:
                    default_code += self.screen_format.code
                    name += " " + self.screen_format.name
                    description += " " + self.screen_format.name
                if self.screen_connectique:
                    default_code += self.screen_connectique.code
                    name += " " + self.screen_connectique.name
                    description += " " + self.screen_connectique.name
                if self.graphic_card_technology:
                    default_code += self.graphic_card_technology.code
                    description += " " + self.graphic_card_technology.name
                    name += " " + self.graphic_card_technology.name
            if self.hbs_category == 'screen' and self.model:
                if '-' in default_code:
                    default_code = default_code.split('-')[0]
                default_code += '-'+self.model.code
                name = "Ecran"
                if self.maker:
                    name += " "+self.maker.name + '-'+self.model.code
                description = name


        return {
            'sku': default_code.strip(),
            'name': name.strip(),
            'description': description.strip()
        }

    @api.model
    def default_get(self, fields):
        result = super(ProductTemplate, self).default_get(fields)
        if 'type' in result:
            result['type'] = 'product'
        return result



class ProductProduct(models.Model):

    _inherit = "product.product"

    hbs_category = fields.Selection(string="Type produit", related="categ_id.hbs_category", store=True)

    @api.onchange('maker', 'grade', 'model', 'cpu', 'screen_resolution',
                  'screen_size', 'keyboard', 'camera', 'categ_id', 'ram_number',
                  'ram_technology', 'ram_size1', 'ram_size2', 'ram_size3', 'ram_size4',
                  'ram_size5', 'ram_size6', 'ram_size7', 'ram_size8', 'hard_disk_technology',
                  'hard_disk_size', 'graphic_card_technology', 'battery',
                  'charger', 'ram_state', 'ram_form_factor', 'cpu_state', 'cpu_core_number',
                  'product_state', 'wide', 'battery_state', 'hard_disk_state', 'screen_connectique', 'screen_format'
                  )
    def onchange_product_details_hbs(self):
        default_code = ""
        name = ""
        description = ""
        if self.model:
            self.screen_size = False
            self.ram_technology = False
            if self.model.screen_size:
                self.screen_size = self.model.screen_size.id
            if self.model.ram_technology:
                self.ram_technology = self.model.ram_technology.id
        # product category
        if self.hbs_category in ("ram", "desktop"):
            if self.ram_form_factor:
                default_code += self.ram_form_factor.code
        if self.hbs_category:
            if self.hbs_category == "tablette":
                default_code += "TBL"
                description += "Tablette"
            elif self.hbs_category == "laptop":
                default_code += "LPT"
                description += "PC Portable"
            elif self.hbs_category == "desktop":
                description += "PC de Bureau"
            elif self.hbs_category == "aio":
                default_code += "AIO"
                description += "AIO"
            elif self.hbs_category == "laptop_barebone":
                default_code += "LPT"
                description += "PC Portable Barebone"
                name += "PC Portable Barebone"
            elif self.hbs_category == "ram":
                default_code += "RAM"
                description += "Carte RAM"
                name += "Carte RAM"
                if self.ram_state:
                    if self.ram_state == "new":
                        default_code += "N"
                    else:
                        default_code += "D"
            elif self.hbs_category == "laptop_battery":
                default_code += "BTL"
                description += "Batterie de PC Portable"
                if self.battery_state:
                    if self.battery_state == "new":
                        default_code += "N"
                    else:
                        default_code += "D"
            elif self.hbs_category == "cpu":
                default_code += "CPU"
                description += "Processeur"
                if self.cpu_state:
                    if self.cpu_state == "new":
                        default_code += "N"
                    else:
                        default_code += "D"
            elif self.hbs_category == "screen":
                default_code += "DSP"
                description += "Ecran"
                if self.product_state:
                    default_code += self.product_state.upper()
            elif self.hbs_category == "hard_disk":
                default_code += "DRV"
                name += "Disque dur"
                if self.hard_disk_state:
                    if self.hard_disk_state == "new":
                        default_code += "N"
                    elif self.hard_disk_state == "occasion":
                        default_code += "D"
                    else:
                        default_code += "R"
            if self.grade:
                default_code += self.grade.code
            if self.maker:
                default_code += self.maker.code
                name += " " + self.maker.name
                description += " " + self.maker.name
            if self.hbs_category == "hard_disk":
                default_code += "-"
            if self.model:
                default_code += "-" + self.model.code
                name += " " + self.model.name
                description += " " + self.model.name
            if self.hbs_category in ("ram", "desktop"):
                if self.ram_form_factor:
                    name += " " + self.ram_form_factor.name
                    description += " " + self.ram_form_factor.name
            if self.screen_size:
                name += " " + self.screen_size.code + '" '
                description += " " + self.screen_size.code + '" '
            if self.screen_resolution:
                if self.hbs_category == "screen" and  self.screen_size:
                    default_code += "-" + self.screen_size.code
                default_code += self.screen_resolution.code
                name += self.screen_resolution.name
                description += self.screen_resolution.name
            if self.cpu:
                default_code += "-" + self.cpu.code
                name += " " + self.cpu.name_code
                description += " " + self.cpu.name

            if self.hbs_category not in ["laptop_barebone"]:
                if self.ram_number  and self.hbs_category != 'screen':

                    size = 0
                    if (int(self.ram_number) >= 1):
                        size += int(self.ram_size1.name)
                    if (int(self.ram_number) >= 2):
                        size += int(self.ram_size2.name)
                    if (int(self.ram_number) >= 3):
                        size += int(self.ram_size3.name)
                    if (int(self.ram_number) >= 4):
                        size += int(self.ram_size4.name)
                    if (int(self.ram_number) >= 5):
                        size += int(self.ram_size5.name)
                    if (int(self.ram_number) >= 6):
                        size += int(self.ram_size6.name)
                    if (int(self.ram_number) >= 7):
                        size += int(self.ram_size7.name)
                    if (int(self.ram_number) >= 8):
                        size += int(self.ram_size8.name)
                    if size != 0:
                        default_code += "-" + str(size).zfill(2)
                        name += " " + str(size) + "GB"
                        description += " " + str(size) + "GB"
                if self.ram_technology:
                    default_code += self.ram_technology.code
                    description += " " + self.ram_technology.name
                if self.hard_disk_size:
                    default_code += self.hard_disk_size.code
                    name += " " + self.hard_disk_size.code + "GB"
                    description += " " + self.hard_disk_size.code + "GB"
                if self.hard_disk_technology:
                    default_code += self.hard_disk_technology.code
                    description += " " + self.hard_disk_technology.name
                    if self.hbs_category == "hard_disk":
                        name += " " + self.hard_disk_technology.name

            if self.keyboard:
                default_code += "-" + self.keyboard.code
                description += " " + self.keyboard.name
            if self.camera:
                default_code += "W"
                description += " Webcam"
            if self.hbs_category == "cpu":
                if self.cpu_core_number:
                    default_code += self.cpu_core_number.code
                    name += " " + self.cpu_core_number.name
                    description += " " + self.cpu_core_number.name
            if self.screen_format:
                default_code += self.screen_format.code
                name += " " + self.screen_format.name
                description += " " + self.screen_format.name
            if self.screen_connectique:
                default_code += self.screen_connectique.code
                name += " " + self.screen_connectique.name
                description += " " + self.screen_connectique.name
            if self.graphic_card_technology:
                default_code += self.graphic_card_technology.code
                description += " " + self.graphic_card_technology.name
                name += " " + self.graphic_card_technology.name
            if self.hbs_category == 'screen' and self.model:
                if '-' in default_code:
                    default_code = default_code.split('-')[0]
                default_code +=  '-'+self.model.code
                name = "Ecran"
                if self.maker:
                    name += " "+self.maker.name + '-'+self.model.code
                description = name


        self.default_code = default_code.strip()
        self.barcode = default_code.strip()
        self.name = name.strip()
        self.description = description.strip()
        self.description_pickingout = description.strip()
        self.description_picking = description.strip()


class ProductDefaultCode(models.Model):
    _name = 'product.default.code'

    name = fields.Char('Code')
    sequence = fields.Char()

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('product.default.code')
        vals['sequence'] = seq
        return super(ProductDefaultCode, self).create(vals)