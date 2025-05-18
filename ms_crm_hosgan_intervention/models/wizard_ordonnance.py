from odoo import fields, models, _,api
from odoo.osv import expression
from odoo import models, fields
import base64


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

    categorie = fields.Selection([
        ('Examens radiologiques', 'Examens radiologiques'),
        ('Chirurgie bariatrique', 'Chirurgie bariatrique'),
        ('Traitement de Tardyferon 80', 'Traitement de Tardyferon 80'),
        ('Drainage lymphatique', 'Drainage lymphatique'),
        ('Enlever les points des suture', 'Enlever les points des suture'),
    ], string="Ordonnance médicale pour")

    def print_ordonnance(self):
        if not self.id:
            raise ValueError("Aucun wizard d'ordonnance trouvé.")
        return self.env.ref('ms_crm_hosgan_intervention.action_report_ordonnance').report_action(self)

    def print_and_send_ordonnance(self):
        if not self.id:
            raise ValueError("Aucun wizard d'ordonnance trouvé.")

        record_name = 'Ordonnance_%s' % (self.partner_id.name or 'unknown')
        pdf_filename = "%s.%s" % (record_name, 'pdf')
        report = self.env.ref('ms_crm_hosgan_intervention.action_report_ordonnance')
        pdf_content, _ = self.env['ir.actions.report']._render_qweb_pdf(report, [self.id])
        encoded_pdf = base64.b64encode(pdf_content).decode('utf-8')
        attachment = self.env['ir.attachment'].create({
            'name': pdf_filename,
            'datas': encoded_pdf,
            'res_model': self._name,
            'res_id': self.id,
            'type': 'binary',
            'mimetype': 'application/pdf',
            'public': False,
        })
        if not self.partner_id or not self.partner_id.email:
            raise ValueError("Aucune adresse email trouvée pour le patient.")
        mail_values = {
            'subject': 'Votre ordonnance',
            'body_html': '<p>Bonjour,<br/>Veuillez trouver ci-joint votre ordonnance.</p>',
            'email_to': self.partner_id.email,
            'attachment_ids': [(4, attachment.id)],}
        self.env['mail.mail'].create(mail_values).send()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Succès',
                'message': 'Ordonnance imprimée et envoyée avec succès.',
                'type': 'success',
                'sticky': False,
            }
        }



    def print_bilan(self):
        if not self.id:
            raise ValueError("Aucun wizard d'ordonnance trouvé.")
        return self.env.ref('ms_crm_hosgan_intervention.action_report_bilan').report_action(self)

    def print_and_send_bilan(self):
        if not self.id:
            raise ValueError("Aucun wizard trouvé.")

        record_name = 'Bilan_%s' % (self.partner_id.name or 'unknown')
        pdf_filename = "%s.%s" % (record_name, 'pdf')

        report = self.env.ref('ms_crm_hosgan_intervention.action_report_bilan')
        pdf_content, _ = self.env['ir.actions.report']._render_qweb_pdf(report, [self.id])
        encoded_pdf = base64.b64encode(pdf_content).decode('utf-8')

        attachment = self.env['ir.attachment'].create({
            'name': pdf_filename,
            'datas': encoded_pdf,
            'res_model': self._name,
            'res_id': self.id,
            'type': 'binary',
            'mimetype': 'application/pdf',
            'public': False,
        })

        if not self.partner_id or not self.partner_id.email:
            raise ValueError("Aucune adresse email trouvée pour le patient.")

        mail_values = {
            'subject': 'Votre bilan',
            'body_html': '<p>Bonjour,<br/>Veuillez trouver ci-joint votre bilan.</p>',
            'email_to': self.partner_id.email,
            'attachment_ids': [(4, attachment.id)],
        }
        self.env['mail.mail'].create(mail_values).send()

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Succès',
                'message': 'Bilan imprimé et envoyé avec succès.',
                'type': 'success',
                'sticky': False,
            }
        }



    def print_ordonnance_medicale(self):
        if not self.id:
            raise ValueError("Aucun wizard d'ordonnance trouvé.")
        return self.env.ref('ms_crm_hosgan_intervention.action_report_ordonnance_medicale').report_action(self)

    def print_and_send_ordonnance_medicale(self):
        if not self.id:
            raise ValueError("Aucun wizard trouvé.")

        record_name = 'OrdonnanceMedicale_%s' % (self.partner_id.name or 'unknown')
        pdf_filename = "%s.%s" % (record_name, 'pdf')

        report = self.env.ref('ms_crm_hosgan_intervention.action_report_ordonnance_medicale')
        pdf_content, _ = self.env['ir.actions.report']._render_qweb_pdf(report, [self.id])
        encoded_pdf = base64.b64encode(pdf_content).decode('utf-8')

        attachment = self.env['ir.attachment'].create({
            'name': pdf_filename,
            'datas': encoded_pdf,
            'res_model': self._name,
            'res_id': self.id,
            'type': 'binary',
            'mimetype': 'application/pdf',
            'public': False,
        })

        if not self.partner_id or not self.partner_id.email:
            raise ValueError("Aucune adresse email trouvée pour le patient.")

        mail_values = {
            'subject': 'Votre ordonnance médicale',
            'body_html': '<p>Bonjour,<br/>Veuillez trouver ci-joint votre ordonnance médicale.</p>',
            'email_to': self.partner_id.email,
            'attachment_ids': [(4, attachment.id)],
        }
        self.env['mail.mail'].create(mail_values).send()

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Succès',
                'message': 'Ordonnance médicale imprimée et envoyée avec succès.',
                'type': 'success',
                'sticky': False,
            }
        }


class WizardOrdonnanceLine(models.Model):
    _name="wizard.ordonnance.line"
    _description="wizard.ordonnance.line"

    ordonnance_id = fields.Many2one("wizard.ordonnance")
    medicament_id = fields.Many2one("ordonnance")
    bilan_id = fields.Many2one("bilan")
    done = fields.Boolean("Done")