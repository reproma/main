from odoo import fields, models


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    equipment_id = fields.Many2one(
        'maintenance.equipment', check_company=True, domain=[('product_id', '!=', False)],
        help="Equipment to be repaired by ticket")

    def action_generate_fsm_task(self):
        """Inherit method to added default_user in fsm task"""
        res = super(HelpdeskTicket, self).action_generate_fsm_task()
        context = res.get('context', {})
        context.update(
            {
                'default_user_id': self.user_id.id,
                'default_equipment_id': self.equipment_id.id,
            }
        )
        progress_stage = self.env.ref('helpdesk.stage_in_progress', raise_if_not_found=False)
        self.action_advance_stage(progress_stage)
        return dict(res, context=context)

    def action_advance_stage(self, stage=False):
        if not stage and len(self.team_id.stage_ids) > 1:  # team without stage (or with only one)
            stage = self.team_id.stage_ids[-1]
        self.write({'stage_id': stage.id})
