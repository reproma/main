from odoo import models


class CreateTask(models.TransientModel):
    _inherit = 'helpdesk.create.fsm.task'

    def action_generate_task(self):
        """Inherit method for to create repair order and maintenance request"""
        task = super(CreateTask, self).action_generate_task()
        equipment_id = task.equipment_id
        equipment_id._create_new_request(equipment_id.next_action_date)
        progress_stage = self.env.ref('maintenance.stage_1', raise_if_not_found=False)
        self.env['maintenance.request'].action_advance_stage(equipment_id, progress_stage)
        task.create_new_repair()
        return task
