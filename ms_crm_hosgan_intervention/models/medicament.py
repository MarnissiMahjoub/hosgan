from odoo import fields, models, _,api
from odoo.osv import expression
from odoo import models, fields

class Ordonnance(models.Model):
    _name = "ordonnance"
    _description = "Ordonnance"
    _order = 'name'

    med_active = fields.Boolean("Médicament active")
    name = fields.Char(string="Nom du médicament",required=True)
    number_day = fields.Integer(string="Nombre de fois par jours")
    pendant = fields.Integer(string="Pendant")
    semaine_jour_mois = fields.Selection([('jour', 'Jour'),('semaine', 'Semaine'),('mois', 'Mois'),],string="Unité de temps" )


