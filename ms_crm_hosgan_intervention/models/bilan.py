from odoo import fields, models, _,api
from odoo.osv import expression
from odoo import models, fields

class Bilan(models.Model):
    _name = "bilan"
    _description = "Bilan"
    _order = 'categorie'

    categorie = fields.Selection([
        ('BILAN BIOLOGIQUE', 'BILAN BIOLOGIQUE'),
        ('EXAMENS RADIOLOGIQUES', 'EXAMENS RADIOLOGIQUES'),
        ('EXAMENS CARDIAQUES', 'EXAMENS CARDIAQUES'),
        ('BILAN BIOLOGIQUE CHIRURGIE BARIATRIQUE', 'BILAN BIOLOGIQUE CHIRURGIE BARIATRIQUE'),
    ], string="Type de Bilan")
    name = fields.Char(string="Nom du Bilan",required=True)
    med_active = fields.Boolean("Bilan active")
