from odoo import fields, models


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    l10n_cr_edi_payment_method = fields.Selection(
        selection=[
            ('01', 'Efectivo / No se sabe'),
            ('02', 'Tarjeta'),
            ('03', 'Cheque'),
            ('04', 'Tranferencia o depósito bancario'),
            ('05', 'Recaudo por terceros'),
            ('99', 'Otros')
        ],
        string='Payment method',
        help="Indicates the way the invoice was/will be paid, where the options could be: "
        "Cash, Credit Card, Nominal Check etc. If unknown, please use cash.",
        default='01'
    )
