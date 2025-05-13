# Copyright © 2021 Garazd Creation (<https://garazd.biz>)

from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    ga4_debug_mode = fields.Boolean(string='Debug Mode')
    gtag_tracking_key = fields.Char(string='Tracking ID')

    def _gtag_params(self):
        self.ensure_one()
        return {'debug_mode': True} if self.ga4_debug_mode else {}

    def _gtag_configs(self):
        self.ensure_one()
        return [{
            'key': self.gtag_tracking_key or '',
            'params': self._gtag_params(),
        }]

    def gtag_get_primary_key(self):
        self.ensure_one()
        return self.gtag_tracking_key or ''
