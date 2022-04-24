# Copyright 2021 Vauxoo
# License AGPL-3 or later (http://www.gnu.org/licenses/agpl).

import werkzeug.urls
from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = 'account.move'

    @api.model
    def l10n_cr_edi_generate_qr_code_url(self):
        super().l10n_cr_edi_generate_qr_code_url()
        url = self.company_id.website or 'https://www.reproma.com'
        qr_code_url = '/report/barcode/?type=%s&value=%s&width=%s&height=%s&humanreadable=1' % (
            'QR', werkzeug.url_quote_plus(url), 80, 80)
        return qr_code_url
