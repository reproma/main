from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    currency_provider = fields.Selection(selection_add=[('bccr', 'Bank of Costa Rica')], ondelete={'bccr': 'set default'})
