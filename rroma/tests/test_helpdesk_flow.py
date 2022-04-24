from .common import RromaTransactionCase


class TestHelpdeskFlow(RromaTransactionCase):
    def setUp(self):
        super().setUp()
        self.project_id = self.env.ref('industry_fsm.fsm_project')
        self.location = self.create_location(self.assigned)
        self.picking_type_id = self.env.ref('stock.picking_type_out')

    def test_01_helpdesk_flow(self):
        """Test case: Helpdesk custom flow

        The following is performed:
        - Helpdesk order
        - Create maintenance and repair order
        - Picking (incoming/outcoming) to the product repaired
        - Message tracking
        """
        helpdesk = self.create_helpdesk(self.customer, self.assigned)
        ctx = helpdesk.action_generate_fsm_task().get('context')
        ctx.update({
            'active_id': helpdesk.id,
            'active_ids': helpdesk.ids,
            'active_model': helpdesk._name,
        })

        wizard = self.env['helpdesk.create.fsm.task'].with_context(ctx).create({})
        task = wizard.action_generate_task()

        # Verify helpdesk with equipment
        equipment_id = task.equipment_id
        self.assertRecordValues(helpdesk, [{
            'stage_id': self.env.ref('helpdesk.stage_in_progress').id,
            'equipment_id': equipment_id.id,
        }])
        self.assertEqual(equipment_id.name, equipment_id.product_id.name)

        # Verify maintenance order
        maintenance_order = task.equipment_id.maintenance_ids
        self.assertRecordValues(maintenance_order, [{
            'stage_id': self.env.ref('maintenance.stage_1').id,
            'equipment_id': equipment_id.id,
            'user_id': helpdesk.user_id.id,
        }])

        # Verify repair order
        repair_order = self.env['repair.order'].search([('task_id', '=', task.id)])
        self.assertRecordValues(repair_order, [{
            'partner_id': task.partner_id.id,
            'state': 'draft',
            'product_id': equipment_id.product_id.id,
            'location_id': self.location.id,
            'user_id': helpdesk.user_id.id,
        }])

        repair_order.action_validate()

        # Verify pickings
        picking_in = repair_order.picking_ids
        self.assertRecordValues(picking_in, [{
            'location_id': self.env.ref('stock.stock_location_customers').id,
            'location_dest_id': self.location.id,
            'origin': repair_order.name,
            'state': 'done',
        }])
        self.assertEqual(picking_in.move_ids_without_package.product_id, repair_order.product_id)

        repair_order.action_repair_start()
        repair_order.action_repair_end()

        # Verify stage of maintenance order
        self.assertEqual(maintenance_order.stage_id, self.env.ref('maintenance.stage_3'))

        picking_out = repair_order.picking_ids.filtered(lambda p: p.picking_type_id.id == self.picking_type_id.id)
        self.assertRecordValues(picking_out, [{
            'location_id': self.location.id,
            'location_dest_id': self.env.ref('stock.stock_location_customers').id,
            'origin': repair_order.name,
            'state': 'done',
        }])
        self.assertEqual(picking_out.move_ids_without_package.product_id, repair_order.product_id)

        repair_order.action_repair_invoice_create()

        # Verify stage of task
        self.assertEqual(task.stage_id, self.env.ref('industry_fsm.planning_project_stage_1'))

        # Verify stage of heklpdesk
        self.assertEqual(helpdesk.stage_id, self.env.ref('rroma.stage_invoiced'))

        # Verify message
        message_ids = helpdesk.message_ids
        self.assertRegex(message_ids[0].body, u'.*The repair order:.*')
