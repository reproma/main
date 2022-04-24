from odoo import fields, models


class Task(models.Model):
    _inherit = "project.task"

    equipment_id = fields.Many2one(
        'maintenance.equipment', check_company=True, help="Equipment to be repaired by ticket")
    repair_id = fields.Many2one('repair.order', help="Technician's repair")

    def _preparare_task_repair_values(self):
        location = self.env['stock.location'].search([('owner_id', '=', self.user_id.id)], limit=1)
        if not location:
            location = self.env.ref('stock.stock_location_stock', raise_if_not_found=False)
        values = {
            'product_id': self.equipment_id.product_id.id,
            'product_uom': self.equipment_id.product_id.uom_id.id,
            'partner_id': self.partner_id.id,
            'user_id': self.user_id.id,
            'task_id': self.id,
            'location_id': location.id if location else False,
            'invoice_method': 'after_repair',
        }
        return values

    def create_new_repair(self):
        repair_obj = self.env['repair.order']
        repair = repair_obj.search([('task_id', '=', self.id)], limit=1)
        if not repair:
            values = self._preparare_task_repair_values()
            repair = self.env['repair.order'].create(values)
        self.repair_id = repair
        return repair
