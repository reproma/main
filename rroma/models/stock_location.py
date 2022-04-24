from odoo import fields, models


class Location(models.Model):
    _inherit = "stock.location"

    owner_id = fields.Many2one('res.users', 'Owner', help="Technician owner of the location if is internal")
