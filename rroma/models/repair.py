from odoo import api, fields, models


class Repair(models.Model):
    _inherit = 'repair.order'

    @api.model
    def _default_stock_location(self):
        """Inherit method for set location of the technical"""
        location = self.env['stock.location'].search([('owner_id', '=', self.env.user.id)], limit=1)
        if location:
            return location.id
        res = super()._default_stock_location()
        return res

    location_id = fields.Many2one(default=_default_stock_location)
    picking_ids = fields.Many2many('stock.picking', string='Receptions', copy=False,
                                   help="Pickings related to the product to be repaired")
    group_id = fields.Many2one('procurement.group', string="Procurement Group", copy=False,
                               help="Procurement group for the product to be repaired")
    task_id = fields.Many2one('project.task', copy=False, help="Technician's task")

    def action_validate(self):
        """Inherited method to create picking of incoming type in product to repair"""
        self._create_picking()
        result = super(Repair, self).action_validate()
        return result

    def action_repair_end(self):
        """Inherited method for create picking of outgoing type in product to repair"""
        result = super(Repair, self).action_repair_end()
        self._create_picking('outgoing')
        equipment_id = self.task_id.equipment_id
        if not equipment_id:
            return result
        repair_stage = self.env.ref('maintenance.stage_3', raise_if_not_found=False)
        self.env['maintenance.request'].action_advance_stage(equipment_id, repair_stage)
        return result

    def action_repair_invoice_create(self):
        """Inherited method for send message to helpdesk linked to the repair"""
        result = super(Repair, self).action_repair_invoice_create()
        for repair in self:
            values = {'fsm_done': True}
            task = repair.task_id
            if task.helpdesk_ticket_id:
                invoiced_stage = self.env.ref('rroma.stage_invoiced', raise_if_not_found=False)
                task.helpdesk_ticket_id.action_advance_stage(invoiced_stage)
            # determine closed stage for task
            closed_stage = task.project_id.type_ids.filtered(lambda stage: stage.is_closed)
            if not closed_stage and len(task.project_id.type_ids) > 1:  # project without stage (or with only one)
                closed_stage = task.project_id.type_ids[-1]
            if closed_stage:
                values['stage_id'] = closed_stage.id
            repair.task_id.write(values)
        return result

    @api.model
    def _prepare_picking(self, operation):
        if not self.group_id:
            self.group_id = self.group_id.create({
                'name': self.name,
                'partner_id': self.partner_id.id
            })
        picking_type_id, location_id, location_dest_id = self._get_locations(operation)

        return {
            'picking_type_id': picking_type_id.id,
            'partner_id': self.partner_id.id,
            'user_id': self.user_id.id,
            'origin': self.name,
            'location_id': location_id.id,
            'location_dest_id': location_dest_id.id,
            'company_id': self.company_id.id,
        }

    def _create_picking(self, operation='incoming'):
        stock_picking = self.env['stock.picking']
        picking = self.picking_ids
        if picking and operation == 'incoming':
            return True
        res = self._prepare_picking(operation)
        picking = stock_picking.create(res)
        moves = self._create_stock_moves(picking)
        moves._action_confirm()
        moves._action_assign()
        for move_line in moves.mapped('move_line_ids'):
            move_line.qty_done = move_line.product_uom_qty
        moves._action_done()
        picking.message_post_with_view('mail.message_origin_link',
                                       values={'self': picking, 'origin': self},
                                       subtype_id=self.env.ref('mail.mt_note').id)
        self.write({'picking_ids': [(4, picking.id, 0)]})
        return True

    def _prepare_stock_moves(self, picking):
        """ Prepare the stock moves data for one order line. This function returns a list of
        dictionary ready to be used in stock.move's create()
        """
        self.ensure_one()
        res = []
        price_unit = self.product_id.standard_price
        picking_type_id, location_id, location_dest_id = self._get_locations(picking.picking_type_id.code)
        description_picking = self.product_id.with_context(
            lang=self.partner_id.lang or self.env.user.lang)._get_description(picking_type_id)
        template = {
            'name': self.name,
            'product_id': self.product_id.id,
            'product_uom': self.product_id.uom_id.id,
            'product_uom_qty': self.product_qty,
            'location_id': location_id.id,
            'location_dest_id': location_dest_id.id,
            'picking_id': picking.id,
            'partner_id': self.partner_id.id,
            'company_id': self.company_id.id,
            'price_unit': price_unit,
            'picking_type_id': picking_type_id.id,
            'group_id': self.group_id.id,
            'origin': self.name,
            'description_picking': description_picking,
            'warehouse_id': picking_type_id.warehouse_id.id,
        }
        res.append(template)
        return res

    def _create_stock_moves(self, picking):
        val = self._prepare_stock_moves(picking)
        return self.env['stock.move'].create(val)

    def _get_locations(self, operation):
        location_customer = self.env.ref('stock.stock_location_customers')
        picking_type_in = self.env.ref('stock.picking_type_in')
        picking_type_out = self.env.ref('stock.picking_type_out')

        picking_type = picking_type_in if operation == 'incoming' else picking_type_out
        location_id = location_customer if operation == 'incoming' else self.location_id
        location_dest_id = self.location_id if operation == 'incoming' else location_customer

        return picking_type, location_id, location_dest_id


class RepairLine(models.Model):
    _inherit = 'repair.line'

    warehouse_id = fields.Many2one('stock.warehouse', compute='_compute_warehouse_id', store=True)
    warehouses_stock = fields.Text(store=False, readonly=True)
    warehouses_stock_recompute = fields.Boolean(store=False)

    @api.depends('repair_id.location_id')
    def _compute_warehouse_id(self):
        for line in self:
            line.warehouse_id = line.repair_id.location_id.get_warehouse()

    def _compute_get_warehouses_stock(self):
        for line in self:
            line.warehouses_stock = line.product_id.with_context(
                warehouse_id=line.warehouse_id,
                force_company=line.warehouse_id.company_id.id)._compute_get_quantity_warehouses_json()

    @api.onchange('warehouses_stock_recompute', 'product_id')
    def _warehouses_stock_recompute_onchange(self):
        if not self.warehouses_stock_recompute:
            self.warehouses_stock_recompute = True
            return
        self._compute_get_warehouses_stock()
        self.warehouses_stock_recompute = True

    @api.onchange('type', 'repair_id')
    def onchange_operation_type(self):
        """Inherit method for set location of the technical if type=add"""
        res = super().onchange_operation_type()
        if self.type == 'add':
            location_id = self.env['stock.location'].search([('owner_id', '=', self.repair_id.user_id.id)], limit=1)
            self.location_id = location_id
        return res
