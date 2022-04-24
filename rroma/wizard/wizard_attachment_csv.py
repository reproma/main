# Copyright 2019 Vauxoo (https://www.vauxoo.com) <info@vauxoo.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64
from odoo import fields, models
from odoo.addons.base.models.ir_ui_view import keep_query


class IrAttachmentcsv(models.TransientModel):
    _name = 'ir.attachment.valuation.layer.csv'
    _description = 'Create CSV file for report stock_valuation_layer'

    csv_row_data = fields.Text()
    csv_file = fields.Binary(readonly=True)
    csv_filename = fields.Char(required=True)

    def _set_csv_file(self):
        if not self.csv_row_data:
            self.csv_file = None
            return
        self.csv_file = base64.b64encode(self.csv_row_data.encode())

    def _get_action_download(self):
        if not self.csv_file:
            return {}
        url_base = "web/content"
        url_data = {
            'model': self._name,
            'id': self.id,
            'filename_field': 'csv_filename',
            'field': 'csv_file',
            'download': 'true',
            'filename': self.csv_filename,
        }
        action = {
            'name': 'Download csv report for stock valuation layer',
            'type': 'ir.actions.act_url',
            'url': "%s/?%s" % (url_base, keep_query(**url_data)),
            'target': 'self',
            'data': url_data,
        }
        return action
