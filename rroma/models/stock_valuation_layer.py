from odoo import models


class StockValuationLayer(models.Model):
    """Stock Valuation Layer"""
    _inherit = 'stock.valuation.layer'

    def action_valuation_layer_report(self, raw_data=False, filename=False, domain=False):
        """This is for return the action to download the csv provided from
        action server side or from the _get_report_valuation_layer_csv
        implementation.
        """
        if not raw_data:
            raw_data = self._get_report_valuation_layer_csv(domain)
        if not filename:
            filename = 'stock_valuation_layer_report.csv'
        attach_csv = self.env['ir.attachment.valuation.layer.csv'].create({
            'csv_row_data': raw_data,
            'csv_filename': filename,
        })
        attach_csv._set_csv_file()
        return attach_csv._get_action_download()

    def _get_report_valuation_layer_csv(self, domain=False):
        """To be implemented: this method should return a csv string, meanwhile
        the csv is provided from the action server side"""
        return False
