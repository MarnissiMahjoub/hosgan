from odoo import fields, models, _,api
from odoo.osv import expression
from odoo import models, fields

class Ordonnance(models.Model):
    _name = "ordonnance"
    _description = "Ordonnance"
    _order = 'name'

    med_active = fields.Boolean("médicament active")
    name = fields.Char(string="Nom du médicament",required=True)
    number_day = fields.Integer(string="Nombre de fois par jour")
    pendant = fields.Integer(string="Pendant")
    semaine_jour_mois = fields.Selection([('jour', 'Jour'),('semaine', 'Semaine'),('mois', 'Mois'),],string="Unité de temps" )


class Bilan(models.Model):
    _name = "bilan"
    _description = "Bilan"
    _order = 'categorie'
    categorie = fields.Selection([
        ('Bilan biologique', 'Bilan biologique'),
        ('Examens radiologiques', 'Examens radiologiques'),
        ('Examens cardiaques', 'Examens cardiaques'),
        ('Bilan biologique chirurgie bariatrique', 'Bilan biologique chirurgie bariatrique'),
    ], string="Type de Bilan")

    name = fields.Char(string="Nom du Bilan",required=True)
    med_active = fields.Boolean("médicament active")
