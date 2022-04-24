from odoo import fields, models


class AccountInvoice(models.Model):

    _inherit = 'account.move'

    def _get_default_l10n_cr_edi_economic_activity(self):
        return False

    def domain_economic_activity(self):
        return []

    l10n_cr_edi_sat_status = fields.Selection(
        selection=[
            ('none', 'State not defined'),
            ('signed', 'Not Synced Yet'),
            ('not_signed', 'Waiting for answer'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected')],
        help='Refers to the status of the invoice inside the SAT system.',
        readonly=True,
        copy=False,
        required=True,
        tracking=True,
        default='none')

    l10n_cr_edi_emission_datetime = fields.Datetime(
        string='Emission date & time',
        help='Refers to the date and time of emission of '
        'the invoice inside the MG system.',
        copy=False)
    l10n_cr_edi_attempts = fields.Integer(
        string='Number of attempts',
        help="Number of Attempts",
        default=0,
        copy=False)
    l10n_cr_edi_security_code = fields.Char(
        string="Security_code",
        help="Security_code",
        size=8,
        copy=False)
    l10n_cr_edi_return_code = fields.Char(
        string="Return code",
        help="Return code",
        copy=False)
    l10n_cr_edi_return_message = fields.Char(
        string="Explanatory message of the state",
        help="Explanatory message of the state")
    l10n_cr_edi_bool = fields.Boolean(
        string='Is eInvoice?',
        help='Is eInvoice?',
        compute='_compute_l10n_cr_edi_bool',
        copy=False)
    l10n_cr_edi_type = fields.Selection([
        ('01', 'Electronic invoice'),
        ('02', 'Electronic debit note'),
        ('03', 'Electronic credit note'),
        ('04', 'Electronic ticket'),
        ('08', 'Electronic purchase invoice'),
        ('09', 'Electronic invoice for export')],
        string='eInvoice document type',
        help='eInvoice document type',
        copy=False)
    l10n_cr_edi_state_treas = fields.Selection(
        selection=[
            ('1', 'Accepted'),
            ('2', 'Parcially accepted'),
            ('3', 'Rejected')
        ],
        string='Treasury acknowledgment',
        help='Treasury acknowledgment',
        copy=False)
    l10n_cr_edi_state_customer = fields.Selection(
        selection=[
            ('1', 'Accepted'),
            ('2', 'Parcially accepted'),
            ('3', 'Rejected'),
        ],
        string='Customer acknowledgment',
        help='Customer acknowledgment',
        default=False, copy=False,)
    l10n_cr_edi_xml_filename = fields.Char(
        string='eInvoice XML Filename',
        help='eInvoice XML Filename',
        copy=False)
    l10n_cr_edi_xml_binary = fields.Binary(
        string='eInvoice XML',
        help='eInvoice XML',
        copy=False)
    l10n_cr_edi_pdf_filename = fields.Char(
        string='eInvoice PDF Filename',
        help='eInvoice PDF Filename',
        copy=False)
    l10n_cr_edi_pdf_binary = fields.Binary(
        string='eInvoice PDF',
        help='eInvoice PDF',
        copy=False)
    l10n_cr_edi_xml_treas_filename = fields.Char(
        string='eInvoice Treasury ack. Filename',
        help='eInvoice Treasury ack. Filename',
        copy=False)
    l10n_cr_edi_xml_treas_binary = fields.Binary(
        string='eInvoice Treasury ack. XML',
        help='eInvoice Treasury ack. XML',
        copy=False)
    l10n_cr_edi_xml_customer_filename = fields.Char(
        string='eInvoice Customer ack. Filename',
        help='eInvoice Customer ack. Filename',
        copy=False)
    l10n_cr_edi_xml_customer_binary = fields.Binary(
        string='eInvoice Customer ack. XML',
        help='eInvoice Customer ack. XML',
        copy=False)
    l10n_cr_edi_consecutive_number_receiver = fields.Char(
        string='consecutive_number_receiver',
        help='consecutive_number_receiver',
        copy=False)
    l10n_cr_edi_full_number = fields.Char(
        string='eInvoice Full Number',
        help='eInvoice Full Number',
        copy=False)
    l10n_cr_edi_ref_type = fields.Selection(
        selection=[
            ('01', 'Anula documento electrónico'),
            ('02', 'Corrige monto'),
            ('04', 'Referencia a otro documento'),
            ('05', 'Sustituye comprobante provisional de contingencia'),
            ('99', 'Otro tipo de referencia')],
        string='eInvoice reference type',
        copy=False,
        help="Select if this document refers to another document.")
    l10n_cr_edi_ref_doc = fields.Selection(
        selection=[
            ('01', 'Documento electrónico'),
            ('05', 'Nota de despacho'),
            ('06', 'Contrato'),
            ('07', 'Procedimiento'),
            ('08', 'Comprobante emitido en contingencia'),
            ('99', 'Otro tipo de documento')],
        string='eInvoice reference document type',
        copy=False,
        help="Select the reference document type.")
    l10n_cr_edi_ref_num = fields.Char(
        string='eInvoice reference document number',
        help='eInvoice reference document number',
        copy=False)
    l10n_cr_edi_ref_reason = fields.Char(
        string='eInvoice reference Reason',
        help='eInvoice reference Reason',
        copy=False)
    l10n_cr_edi_reference_datetime = fields.Datetime(
        string='eInvoice reference date and time of issue',
        help='eInvoice reference date and time of issue',
        copy=False)
    l10n_cr_edi_ref_id = fields.Many2one(
        'account.move',
        string='eInvoice reference document',
        help='eInvoice reference document',
        copy=False)
    l10n_cr_edi_economic_activity_id = fields.Many2one(
        'l10n.cr.account.invoice.economic.activity',
        string="Economic Activity",
        help="Economic Activity",
        default=_get_default_l10n_cr_edi_economic_activity,
        domain=lambda self: self.domain_economic_activity())
    l10n_cr_edi_purchase_export_einvoice = fields.Boolean(
        string="Purchase or Export einvoice",
        help="Purchase or Export einvoice",
        default="False")
    l10n_cr_edi_tax_exemption_id = fields.Many2one(
        'l10n_cr_edi.tax.exemption',
        'Tax Exemption',
        help="Indicates the exemption general for the invoice. "
        "If several exonerations are required, please use the exemption field in each invoice line.",)

    l10n_cr_edi_payment_method = fields.Selection(
        selection=[
            ('01', 'Efectivo / No se sabe'),
            ('02', 'Tarjeta'),
            ('03', 'Cheque'),
            ('04', 'Tranferencia o depósito bancario'),
            ('05', 'Recaudo por terceros'),
            ('99', 'Otros')
        ],
        string='eInvoice payment method',
        help='eInvoice payment method',
        default='01')

    l10n_cr_edi_presentation_position = fields.Selection(
        selection=[
            ('1', 'Normal'),
            ('2', 'Contingencia'),
            ('3', 'Sin Internet')
        ],
        string='eInvoice presentation position',
        help='eInvoice presentation position',
        default='1')

    l10n_cr_edi_sale_condition = fields.Selection(
        selection=[
            ('01', 'Cash'),
            ('02', 'Credit'),
            ('03', 'Consignment'),
            ('04', 'Set aside'),
            ('05', 'Lease with purchase option'),
            ('06', 'Lease in financial function'),
            ('07', 'Payment to a third party'),
            ('08', 'Services provided to the State on credit'),
            ('09', 'Service payments provided to the State'),
            ('99', 'Others')
        ],
        string='eInvoice sale conditions',
        help='eInvoice sale conditions',
        default='01')

    l10n_cr_edi_rel_document_type = fields.Selection(
        string='Journal document type',
        help='Journal document type',
        related='journal_id.l10n_cr_edi_document_type',
        store=False,
        readonly=True)
    l10n_cr_currency_rate = fields.Float(
        string="Currency rate for invoicing in CR",
        help="Currency rate for invoicing in CR")

    l10n_cr_edi_dgt_answer_sent = fields.Boolean(
        readonly=True, default=False, copy=False,
        help="It indicates that the DGT Answer XML for this invoice has been sent.")

    def _compute_l10n_cr_edi_bool(self):
        self.write({'l10n_cr_edi_bool': False})

    def l10n_cr_edi_is_required(self):
        self.ensure_one()
        return self.company_id.country_id == self.env.ref('base.cr')

    def l10n_cr_edi_amount_to_text(self):
        """Method to transform a float amount to text words
        E.g. 100.10 - One Hundread with 10/100 (Colons)
        :returns: Amount transformed to words costarican format for invoices
        :rtype: str
        """
        self.ensure_one()
        return "TODO"

    def l10n_cr_edi_get_xml_etree(self, xml=None):
        return None

    def l10n_cr_edi_generate_qr_code_url(self):
        return False


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    l10n_cr_edi_tax_exemption_id = fields.Many2one(
        'l10n_cr_edi.tax.exemption',
        'Tax Exemption',
        help="Indicates the exemption for this line if is different to the general in the invoice.")
