# -*- coding: utf-8 -*-

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
            ('feedback', "Feedback"),
            ('avis_google_business','Avis sur Google Business'),
            ('transfusion_consent', "CONSENTEMENT POUR TRANSFUSION SANGUINE"),
            ('reception_dossier_medical', "CONFIRMATION DE RÉCEPTION DU DOSSIER MÉDICAL"),
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
                <p>Pour compléter votre dossier, nous vous demandons de signer l'autorisation d'usage des
photos avant et après votre intervention.</p>
                <p>Merci de votre collaboration et à très bientôt.</p>
                <p>Cordialement.</p>
                <p>L’équipe HOSGAN.</p>
            """.format(name=self.partner_id.name)

        elif self.report_selection == "video_testimony":
            record_name = "AUTORISATION D'UTILISATION DU TÉMOIGNAGE VIDÉO " + self.partner_id.name
            report = self.env.ref('sm_hosgan_intervention_autorisation_report.action_report_video_authorization')
            email_subject = "Autorisation d’utilisation de témoignage vidéo"
            email_body = """
                <p>Bonjour {name},</p>
                <p>Nous vous remercions pour votre confiance! Pour partager votre expérience, nous vous
demandons de signer l'autorisation d'usage des vidéos témoignage.</p>
                            <p>Merci de votre collaboration et à très bientôt..</p>
                <p>Cordialement.</p>
                <p>L’équipe HOSGAN.</p>
            """.format(name=self.partner_id.name)

        elif self.report_selection == "avis_google_business":
            if self.partner_id.lang in ("it_IT", "it"):
                email_subject = "Condividi la tua esperienza e lasciaci una recensione"
                email_body = f"""
                    <p>Ciao {self.partner_id.name},</p>
                    <p>Ci auguriamo che tu sia soddisfatta dei tuoi risultati!</p>
                    <p>Ti saremmo molto grati se potessi lasciarci una recensione su Google Business e seguirci sui nostri social per rimanere aggiornato sulle ultime novità.</p>
                    <p>
                        <a href="https://g.page/r/xxxxxxxx">Lascia una recensione su Google</a><br/>
                        Seguici su <a href="https://instagram.com/hosgan">Instagram</a>, 
                        <a href="https://tiktok.com/@hosgan">TikTok</a> e 
                        <a href="https://facebook.com/hosgan">Facebook</a>.
                    </p>
                    <p>Grazie ancora per la tua fiducia!</p>
                    <p>Cordiali saluti,<br/>L’équipe HOSGAN</p>
                """
            else:  # Par défaut en français
                email_subject = "Partagez votre expérience et laissez un avis"
                email_body = f"""
                    <p>Bonjour {self.partner_id.name},</p>
                    <p>Nous espérons que vous êtes satisfaite de vos résultats !</p>
                    <p>Nous vous serions très reconnaissants si vous pouviez laisser un avis sur notre Google Business et vous abonner à nos réseaux sociaux pour suivre nos dernières actualités.</p>
                    <p>
                        <a href="https://g.page/r/xxxxxxxx">Laisser un avis sur Google</a><br/>
                        Suivez-nous sur <a href="https://instagram.com/hosgan">Instagram</a>,
                        <a href="https://tiktok.com/@hosgan">TikTok</a> et 
                        <a href="https://facebook.com/hosgan">Facebook</a>.
                    </p>
                    <p>Merci encore pour votre confiance !</p>
                    <p>Cordialement,<br/>L’équipe HOSGAN</p>
                """



        elif self.report_selection == "transfusion_consent":
            report = self.env.ref('sm_hosgan_intervention_autorisation_report.action_report_consentement_transfusion')
            record_name = f"CONSENTEMENT TRANSFUSION SANGUINE {self.partner_id.name}"
            email_subject = "Consentement transfusion sanguine à signer"
            email_body = f"""
                <p>Bonjour {self.partner_id.name},</p>
                <p>Veuillez trouver ci-joint le document de consentement concernant une éventuelle transfusion sanguine durant l'intervention. Merci de le lire attentivement et de le signer.</p>
               <p>Cordialement.</p>
            """



        elif self.report_selection == "reception_dossier_medical":

            report = self.env.ref('sm_hosgan_intervention_autorisation_report.action_report_medical_file_receipt')

            record_name = f"RECEPTION_DOSSIER_MEDICAL_{(self.partner_id.name or '').replace(' ', '_')}"

            if self.partner_id.lang == "it_IT":

                email_subject = "Conferma di ricezione della documentazione medica"

                email_body = f"""

                    <p>Gentile {self.partner_id.name},</p>

                    <p>La ringraziamo per aver scelto i nostri servizi.</p>

                    <p>In allegato troverà il documento di conferma di ricezione della documentazione medica.</p>

                    <p>La invitiamo a conservarlo con cura.</p>

                    <p>Cordiali saluti,</p>

                    <p>Il team medico HOSGAN</p>

                """

            else:

                email_subject = "Confirmation de réception du dossier médical"

                email_body = f"""

                    <p>Bonjour {self.partner_id.name},</p>

                    <p>Merci de votre confiance.</p>

                    <p>Veuillez trouver ci-joint le document de confirmation de réception de votre dossier médical.</p>

                    <p>Nous vous invitons à le conserver précieusement.</p>

                    <p>Cordialement,</p>

                    <p>L'équipe médicale HOSGAN</p>

                """




        elif self.report_selection == "feedback":
            report = self.env.ref('sm_hosgan_intervention_autorisation_report.action_report_feedback')
            record_name = f"FEEDBACK {self.partner_id.name}"
            email_subject = "Votre retour d'expérience - Feedback"
            email_body = f"""
                <p>Bonjour {self.partner_id.name},</p>
                <p>Nous vous remercions pour votre confiance.</p>
                <p>Veuillez trouver ci-joint un formulaire de feedback concernant votre intervention. Nous vous serions reconnaissants de bien vouloir le remplir et le retourner.</p>
                <p>Votre avis est précieux pour améliorer la qualité de nos services.</p>
                <p>Cordialement,</p>
                <p>L'équipe médicale</p>

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
        if self.report_selection == "avis_google_business":
            mail_values = {
                'subject': email_subject,
                'body_html': email_body,
                'email_to': self.partner_id.email,

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




