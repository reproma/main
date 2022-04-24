# Copyright 2016 Vauxoo
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    l10n_cr_edi_test_env = fields.Boolean(
        related='company_id.l10n_cr_edi_test_env', string="CR PAC test environment",
        readonly=False,
        help='Enable when the certificate environment is test')

    l10n_cr_edi_client_api_key = fields.Char(
        related='company_id.l10n_cr_edi_client_api_key', readonly=False)
