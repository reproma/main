# Copyright 2021 Vauxoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    shipping_instructions = fields.Selection([
        ('air_freight', 'Air Freight'),
        ('sea_freaight', 'Sea Freight'),
        ('ground_best_way', 'Ground Best Way'),
        ('ups_third_day', 'Third Day'),
        ('ups_second_day', 'Second Day'),
        ('ups_next_day', 'Next Day'),
        ('dhl_account_number', 'DHL Account #951482852'),
        ('nex_day_to_be_advised', 'To be advised'),
        ('fedex_third_day', 'NO USAR - Fedex Third Day'),
        ('fedex_second_day', 'NO USAR - Fedex Second Day'),
        ('fedex_next_day', 'NO USAR - Fedex Next Day'),
        ('dhl_third_day', 'NO USAR - Third Day DHL #951482852'),
        ('dhl_second_day', 'NO USAR - Second Day DHL #951482852'),
        ],
        copy=False,
        help="This is the shipping instructions for the purchase order.")

    door_to_door = fields.Selection([
        ('air_best_way', 'Air Best Way'),
        ('truck_best_way', 'Truck Best Way'),
        ('ocean_best_way', 'Ocean Best Way')],
        copy=False,
        help="This is the door to door instructions for this purchase order.")

    door_to_port = fields.Selection([
        ('air_best_way', 'Air Best Way'),
        ('truck_best_way', 'Truck Best Way'),
        ('ocean_best_way', 'Ocean Best Way')],
        copy=False,
        help="This is the door to port instructions for this purchase order.")

    alternate_shipping_address_id = fields.Many2one(
        'res.partner', help="Alternative shipping address, to show in the purchase reports.")
