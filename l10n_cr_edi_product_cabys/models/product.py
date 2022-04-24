# Copyright 2020 Vauxoo
# License LGPL-3 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models


class L10nCrEdiProductCabys(models.Model):

    _name = 'l10n.cr.edi.product.cabys'
    _description = "Product and Service Codes from DGT Data"

    code = fields.Char(
        help='This value is required in all eInvoicing XML version 4.3 to express the code of the '
        'product or service covered by the present concept. Must be used a key from the DGT catalog (CABYS).',
        required=True)
    name = fields.Char(
        help='Name defined by DGT CABYS for this product',
        required=True)
    tax_amount = fields.Char(help="Tax amount")
    active = fields.Boolean(
        help='If this record is not active, this cannot be selected.',
        default=True)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    l10n_cr_edi_code_cabys_id = fields.Many2one(
        'l10n.cr.edi.product.cabys', 'CABYS code',
        help='This value is required in all eInvoicing XML version 4.3 to express the code of the '
        'product or service covered by the present concept. Must be used a key from the DGT catalog (CABYS).')
