from odoo import api, fields, models


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    equipment_assign_to = fields.Selection(
        selection_add=[('customer', 'Customer')], default='customer', ondelete={'customer': 'set default'}
    )
    customer_id = fields.Many2one('res.partner', check_company=True, help="Client, equipment owner")
    maintenance_team_id = fields.Many2one(default=lambda self: self.env.ref('maintenance.equipment_team_maintenance'))
    product_id = fields.Many2one(
        'product.product', check_company=True, help="Allows the management of equipment in locations"
    )

    @api.onchange('category_id')
    def _onchange_category_id(self):
        """Inherited method to set technician_user_id from helpdesk"""
        res = super()._onchange_category_id()
        if not self.category_id:
            technician_user = self._context.get('default_technician_user_id')
            self.technician_user_id = technician_user
        return res

    @api.model
    def create(self, vals):
        """Inherited method to quickly create a product from helpdesk or equipment"""
        if vals.get('equipment_assign_to', '') != 'customer' and not self._context.get('helpdesk'):
            return super(MaintenanceEquipment, self).create(vals)
        values_product = self._prepare_product_values(vals)
        product_id = self.env['product.product'].create(values_product)
        vals.update({'product_id': product_id.id})
        return super(MaintenanceEquipment, self).create(vals)

    def write(self, vals):
        """Inherited method to quickly write a product from equipment"""
        if self.product_id and self.equipment_assign_to == 'customer':
            values_product = self._prepare_product_values(vals)
            self.product_id.write(values_product)
        return super(MaintenanceEquipment, self).write(vals)

    def _prepare_product_values(self, vals):
        values_product = {
            'type': 'product',
            'sale_ok': False,
            'purchase_ok': False,
            'name': vals.get('name') or self.name,
            'categ_id': self.env.ref('rroma.product_category_repairable').id,
            'standard_price': 0.0,
            'default_code': vals.get('serial_no') or self.serial_no,
        }
        return values_product


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    @api.model
    def action_advance_stage(self, equipment_id, stage):
        maintenance_ids = self.env['maintenance.request'].search(
            [('stage_id.done', '=', False), ('equipment_id', '=', equipment_id.id)])
        if stage:
            maintenance_ids.write({'stage_id': stage.id})
