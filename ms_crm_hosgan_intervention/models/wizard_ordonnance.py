from odoo import fields, models, _,api
from odoo.osv import expression
from odoo import models, fields


class WizardOrdonnance(models.Model):
    _name="wizard.ordonnance"
    _description="wizard.ordonnance"

    def _default_example_date(self):
        return fields.Date.today()
    
    partner_id = fields.Many2one('res.partner', string='Client')
    date = fields.Date(string='Date ', default=_default_example_date, store=True)
    operation = fields.Char("Operation")
    ordonnance_line_ids = fields.One2many("wizard.ordonnance.line","ordonnance_id")
    days_number = fields.Integer("Nombre de jours")
    medecin_id = fields.Many2one('res.partner', string='Médecin')

    def print_ordonnance(self):
        if not self.id:
            raise ValueError("Aucun wizard d'ordonnance trouvé.")
        return self.env.ref('ms_crm_hosgan_intervention.action_report_ordonnance').report_action(self)

    def print_bilan(self):
        if not self.id:
            raise ValueError("Aucun wizard d'ordonnance trouvé.")
        return self.env.ref('ms_crm_hosgan_intervention.action_report_bilan').report_action(self)

    def print_ordonnance_medicale(self):
        if not self.id:
            raise ValueError("Aucun wizard d'ordonnance trouvé.")
        return self.env.ref('ms_crm_hosgan_intervention.action_report_ordonnance_medicale').report_action(self)


class WizardOrdonnanceLine(models.Model):
    _name="wizard.ordonnance.line"
    _description="wizard.ordonnance.line"

    ordonnance_id = fields.Many2one("wizard.ordonnance")
    medicament_id = fields.Many2one("ordonnance")
    bilan_id = fields.Many2one("bilan")
    done = fields.Boolean("Done")