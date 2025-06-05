from odoo import fields, models, _,api
from odoo.osv import expression
from odoo import models, fields


class InterventienTags(models.Model):
    _name="interventien.tags"
    _description = "name"
    _order = 'name'

    name = fields.Char("Nom" ,translate=True)
    categorie = fields.Selection([
        ('seins', 'SEINS'),
        ('corps', 'CORPS'),
        ('visage', 'VISAGE'),
        ('chirurgie_intimes', 'CHIRURGIE INTIMES'),
        ('greffes_cheveux', 'GREFFES DE CHEVEUX'),
        ('chirurgie_bariatrique', 'CHIRURGIE BARIATRIQUE'),
        ('ophtalmologie', 'OPHTALMOLOGIE'),
        ('chirurgie_dentaire', 'CHIRURGIE DENTAIRE'),
        ('medecine_esthetique', 'MEDECINE ESTHETIQUE'),
        ('tecnologie', 'TECNOLOGIE'),
    ], string="Catégorie")
