# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class res_company(models.Model):
    _inherit = "res.company"

    purchase_template = fields.Selection([
            ('fency', 'Fency'),
            ('classic', 'Classic'),
            ('modern', 'Modern'),
            ('odoo_standard', 'Odoo Standard'),
        ], 'Purchase')


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def print_quotation(self):
        self.write({'state': "sent"})
        return self.env.ref('purchase_order_report_templates.custom_report_purchase_quotation').report_action(self)

