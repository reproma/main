from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    l10n_cr_edi_vat_type = fields.Selection([
        ('01', 'Costarican citicen ID'),
        ('02', 'Legal entity'),
        ('03', 'DIMEX'),
        ('04', 'NITE'),
        ('XX', 'Foreigner')],
        string='ID type', help="ID type for CR eInvoicing.")
    # TODO onchange city en blanco en CR
    l10n_cr_edi_canton_id = fields.Many2one(
        'res.country.state.canton', ondelete='restrict')
    l10n_cr_edi_district_id = fields.Many2one(
        'res.country.state.canton.district', ondelete='restrict')
    l10n_cr_edi_neighborhood_id = fields.Many2one(
        'res.country.state.canton.district.neighborhood',
        ondelete='restrict')
    l10n_cr_edi_payment_method = fields.Selection(
        selection=[
            ('01', 'Cash / It is not known'),
            ('02', 'Card'),
            ('03', 'Check'),
            ('04', 'Bank transfer or deposit'),
            ('05', 'Raised by third parties'),
            ('99', 'Others')
        ],
        string='eInvoice payment method')
    l10n_cr_edi_dgt_answer_mail = fields.Boolean(
        string='DGT Answer required?', default=True,
        help="Set active to Send by email the DGT Answer XML File when system receive the document.",)


class ResCountryStateCanton(models.Model):
    _description = "Canton"
    _name = 'res.country.state.canton'
    _order = 'code'

    state_id = fields.Many2one('res.country.state', string='State', required=True)
    name = fields.Char(
        string='Canton Name', required=True,
        help='Administrative divisions of a state. '
        'Used also for CR eInvoicing.')
    code = fields.Char(string='Canton Code',
                       help='The canton code.', required=True)


class ResCountryStateCantonDistrict(models.Model):
    _description = "District"
    _name = 'res.country.state.canton.district'
    _order = 'code'

    l10n_cr_edi_canton_id = fields.Many2one(
        'res.country.state.canton', string='Canton', required=True)
    name = fields.Char(string='District Name', required=True,
                       help='Administrative divisions of a Canton. '
                       'Used also for CR eInvoicing.')
    code = fields.Char(string='Discrict Code', help='The district code.',
                       required=True)

    _sql_constraints = [
        ('name_code_uniq', 'unique(l10n_cr_edi_canton_id, code)',
         'The code of the district must be unique by canton!')
    ]


class ResCountryStateCantonDistrictNeigh(models.Model):
    _description = "Neighborhood"
    _name = 'res.country.state.canton.district.neighborhood'
    _order = 'code'

    district_id = fields.Many2one('res.country.state.canton.district', string='District', required=True)
    name = fields.Char(string='Neighborhood Name', required=True,
                       help='Administrative divisions of a district. '
                       'Used also for CR eInvoicing.')
    code = fields.Char(string='Neighborhood Code',
                       help='The neighborhood code.', required=True)
