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


class CrmLead(models.Model):
    _inherit = "crm.lead"

    @api.depends("interventien_id")
    def intervention_numer(self):
        for record in self :
                record.intervention_number = len(record.interventien_id or [])

    interventien_id = fields.One2many("x_hosgan_intervention","x_studio_many2one_field_61b_1i8f40cvb")

    interventien_tags_ids = fields.Many2many(
        "interventien.tags",
        "crm_id",  # champ Many2one dans l'enfant
        string="Tags d’intervention"
    )

    intervention_number = fields.Integer("Nombre d'intervention",compute="intervention_numer")

    def intervention(self):
        list=[]
        for record in self :
            list.extend(record.interventien_id.ids)
        if list :
            return {
                "name": "Hosgan Intervention",
                "type": "ir.actions.act_window",
                "res_model": "x_hosgan_intervention",
                "view_mode": "list,form",
                "target": "current",
                "domain": [("id", "in", list)],
            }
        return True

    def wizard_ordonnance_medicament(self):
        medicament_list = []
        for record in self.env["ordonnance"].search([("med_active", "=", True)]):
            medicament_list.append((0, 0, {"ordonnance_id": self.env.context.get('active_id'), "medicament_id": record.id, "done": False}))

        return {
            "name": "Ordonnance Medicament",

            "type": "ir.actions.act_window",
            "res_model": "wizard.ordonnance",
            "view_mode": "form",
            "view_type": "form",
            "target": "new",
            "view_id": self.env.ref("ms_crm_hosgan_intervention.view_wizard_ordonnance_form").id,
            "context": {
                "default_partner_id": self.partner_id.id,
                "default_operation": self.name,
                "default_ordonnance_line_ids": medicament_list,
            },
        }


    def wizard_bilan(self):
        bilan_list = []
        for record in self.env["bilan"].search([("med_active", "=", True)]):
            bilan_list.append((0, 0, {"ordonnance_id": self.env.context.get('active_id'), "bilan_id": record.id, "done": False}))

        return {
            "name": "BILANS PRE OPERATOIRES",

            "type": "ir.actions.act_window",
            "res_model": "wizard.ordonnance",
            "view_mode": "form",
            "view_type": "form",
            "target": "new",
            "view_id": self.env.ref("ms_crm_hosgan_intervention.view_wizard_bilan_form").id,
            "context": {
                "default_partner_id": self.partner_id.id,
                "default_operation": self.name,
                "default_ordonnance_line_ids": bilan_list,
            },
        }

    def wizard_ordonnance_medicale(self):

        return {
            "name": "Ordonnance ",

            "type": "ir.actions.act_window",
            "res_model": "wizard.ordonnance",
            "view_mode": "form",
            "view_type": "form",
            "target": "new",
            "view_id": self.env.ref("ms_crm_hosgan_intervention.view_wizard_ordonnance_medicale_form").id,
            "context": {
                "default_partner_id": self.partner_id.id,
                "default_operation": self.name,
            },
        }