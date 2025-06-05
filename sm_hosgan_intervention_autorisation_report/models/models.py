from odoo import models, fields, api
import base64

class sm_hosgan_intervention_autorisation_report(models.Model):
    _name = "report.autorisation"
    _description = "report.autorisation"

    partner_id = fields.Many2one('res.partner', string='Client')
    date_naissance = fields.Date(string='Date de naissance',  store=True)
    report_selection = fields.Selection(
        [
            ('video_testimony', "AUTORISATION D’UTILISATION DU TÉMOIGNAGE VIDÉO"),
            ('before_after_photos', "AUTORISATION D’UTILISATION DES PHOTOS AVANT ET APRÈS"),
            ('consentement_eclaire', "CONSENTEMENT ÉCLAIRÉ"),
            ('transfusion_consent', "CONSENTEMENT POUR TRANSFUSION SANGUINE"),
        ],
        string="Rapport"
    )
    url_pdf = fields.Text("URL PDF")


    # @api.onchange('partner_id','date_naissance',"report_selection")
    # def onchange_url_pdf(self):
    #     self.ensure_one()
    #     self.url_pdf = False

    #
    # def print_autorisation_report(self):
    #     if self :
    #         if self.report_selection == "before_after_photos":
    #             return self.env.ref('sm_hosgan_intervention_autorisation_report.action_report_photo_authorization').report_action(self)
    #         elif self.report_selection == "video_testimony":
    #             return self.env.ref('sm_hosgan_intervention_autorisation_report.action_report_video_authorization').report_action(self)
    #         elif self.report_selection == "consentement_eclaire":
    #             return self.env.ref('sm_hosgan_intervention_autorisation_report.action_report_consentement_necrose').report_action(self)

    def print_and_send_autorisation_report(self):
        if not self.id:
            raise ValueError("Aucun wizard trouvé.")

        if not self.partner_id or not self.partner_id.email:
            raise ValueError("Aucune adresse email trouvée pour le patient.")

        if self.report_selection == "before_after_photos":
            record_name = "AUTORISATION D'UTILISATION DES PHOTOS AVANT ET APRÈS " + self.partner_id.name
            report = self.env.ref('sm_hosgan_intervention_autorisation_report.action_report_photo_authorization')
            email_subject = "Autorisation d’utilisation des photos avant/après"
            email_body = """
                <p>Bonjour {name},</p>
                <p>Veuillez trouver ci-joint le document à signer concernant l'utilisation de vos photos avant/après. Merci de le lire attentivement.</p>
                <p>Cordialement.</p>
            """.format(name=self.partner_id.name)

        elif self.report_selection == "video_testimony":
            record_name = "AUTORISATION D'UTILISATION DU TÉMOIGNAGE VIDÉO " + self.partner_id.name
            report = self.env.ref('sm_hosgan_intervention_autorisation_report.action_report_video_authorization')
            email_subject = "Autorisation d’utilisation de témoignage vidéo"
            email_body = """
                <p>Bonjour {name},</p>
                <p>Veuillez trouver ci-joint le document à signer pour autoriser l'utilisation de votre témoignage vidéo. Merci de le lire attentivement et de nous le retourner signé.</p>
                <p>Cordialement.</p>
            """.format(name=self.partner_id.name)

        elif self.report_selection == "transfusion_consent":
            report = self.env.ref('sm_hosgan_intervention_autorisation_report.action_report_consentement_transfusion')
            record_name = f"CONSENTEMENT TRANSFUSION SANGUINE {self.partner_id.name}"
            email_subject = "Consentement transfusion sanguine à signer"
            email_body = f"""
                <p>Bonjour {self.partner_id.name},</p>
                <p>Veuillez trouver ci-joint le document de consentement concernant une éventuelle transfusion sanguine durant l'intervention. Merci de le lire attentivement et de le signer.</p>
               <p>Cordialement.</p>
            """


        else:
            record_name = "CONSENTEMENT ÉCLAIRÉ " + self.partner_id.name
            report = self.env.ref('sm_hosgan_intervention_autorisation_report.action_report_consentement_necrose')
            email_subject = "Consentement éclairé à signer"
            email_body = """
                <p>Bonjour {name},</p>
                <p>Veuillez trouver ci-joint le formulaire de consentement éclairé concernant votre intervention. Merci de le lire attentivement et de nous le retourner signé.</p>
                <p>Cordialement.</p>
            """.format(name=self.partner_id.name)

        # Génération du PDF
        pdf_filename = "%s.pdf" % record_name
        pdf_content, _ = self.env['ir.actions.report']._render_qweb_pdf(report, [self.id])
        encoded_pdf = base64.b64encode(pdf_content).decode('utf-8')

        attachment = self.env['ir.attachment'].create({
            'name': pdf_filename,
            'datas': encoded_pdf,
            'res_model': self._name,
            'res_id': self.id,
            'type': 'binary',
            'mimetype': 'application/pdf',
            'public': True,
        })

        # Générer l’URL publique (facultatif si tu n’utilises pas dans l’email)
        self.write({
            'url_pdf': f"https://c.hosgan.com/web/content/{attachment.id}?download=true"
        })

        # Envoi de l'email
        mail_values = {
            'subject': email_subject,
            'body_html': email_body,
            'email_to': self.partner_id.email,
            'attachment_ids': [(4, attachment.id)],
        }
        self.env['mail.mail'].create(mail_values).send()

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Succès',
                'message': "Le document a été imprimé et envoyé avec succès.",
                'type': 'success',
                'sticky': False,
            }
        }

    def ouvrir_url(self):
        self.ensure_one()
        return {
            'name': 'URL du PDF',
            "type": "ir.actions.act_window",
            'res_model': 'report.autorisation',
            "view_mode": "form",
            "view_type": "form",
            "target": "new",
            "view_id": self.env.ref("sm_hosgan_intervention_autorisation_report.view_wizard_report_wizard").id,
            'context': {'default_url_pdf': self.url_pdf},
        }




