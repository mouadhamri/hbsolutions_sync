# -*- coding: utf-8 -*-

from odoo import fields, models, api


class HbsModel(models.Model):
    _name = "hbs.model"

    name = fields.Char(string="Nom modèle", required=True)
    code = fields.Char(string="N° du modèle (SKU)", required=True)
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
        ('aio', 'aoi')
    ], string='Catégorie produit')
    screen_size = fields.Many2one("hbs.screen.size", string="Taille écran")
    ram_technology = fields.Many2one("hbs.ram.technology", string="Technologie RAM")


class HbsScreenSize(models.Model):
    _name = "hbs.screen.size"

    name = fields.Char(string="Nom taille", required=True)
    code = fields.Char(string="Code (SKU)", required=True)


class HbsRamTechnology(models.Model):
    _name = "hbs.ram.technology"

    name = fields.Char(string="Technologie RAM", required=True)
    code = fields.Char(string="Code (SKU)", required=True)


class HbsMaker(models.Model):
    _name = "hbs.maker"

    name = fields.Char(string="Nom fabricant", required=True)
    code = fields.Char(string="Code (SKU)", required=True)


class HbsGrade(models.Model):
    _name = "hbs.grade"

    name = fields.Char(string="Nom grade", required=True)
    code = fields.Char(string="Code (SKU)", required=True)


class HbsCPU(models.Model):
    _name = "hbs.cpu"

    name = fields.Char(string="Nom CPU", required=True)
    code = fields.Char(string="Code (SKU)", required=True)
    name_code = fields.Char(string="Code (Nom article)")


class HbsCoreNumber(models.Model):
    _name = "hbs.core.number"

    name = fields.Char(string="Nom Nombre de core", required=True)
    code = fields.Char(string="Code (SKU)", required=True)



class HbsScreenResolution(models.Model):
    _name = "hbs.screen.resolution"

    name = fields.Char(string="Nom résolution écran", required=True)
    code = fields.Char(string="Code (SKU)", required=True)


class HbsRamSize(models.Model):
    _name = "hbs.ram.size"

    name = fields.Char(string="Taille RAM", required=True)
    code = fields.Char(string="Code (SKU)", required=True)


class HbsFormFactor(models.Model):
    _name = "hbs.form.factor"

    name = fields.Char(string="Nom facteur de forme", required=True)
    code = fields.Char(string="Code (SKU)", required=True)


class HbsHardDiskTechnology(models.Model):
    _name = "hbs.hard.disk.technology"

    name = fields.Char(string="Technologie Disque dur", required=True)
    code = fields.Char(string="Code (SKU)", required=True)

class HbsHardDiskSize(models.Model):
    _name = "hbs.hard.disk.size"

    name = fields.Char(string="Taille Disque dur", required=True)
    code = fields.Char(string="Code (SKU)", required=True)

class HbsGraphicCardTechnology(models.Model):
    _name = "hbs.graphic.card.technology"

    name = fields.Char(string="Nom", required=True)
    code = fields.Char(string="Code (SKU)", required=True)

class HbsGraphicCardSize(models.Model):
    _name = "hbs.graphic.card.size"

    name = fields.Char(string="Taille Carte graphique", required=True)
    code = fields.Char(string="Code (SKU)", required=True)


class HbsKeyboard(models.Model):
    _name = "hbs.keyboard"

    name = fields.Char(string="Nom clavier", required=True)
    code = fields.Char(string="Code (SKU)", required=True)


class HbsScreenConnectique(models.Model):
    _name = 'hbs.screen.connectique'

    name = fields.Char(string="Connectique", required=True)
    code = fields.Char(string="Code (SKU)", required=True)


class HbsScreenFormat(models.Model):
    _name = 'hbs.screen.format'

    name = fields.Char(string="Format d'écran", required=True)
    code = fields.Char(string="Code (SKU)", required=True)
