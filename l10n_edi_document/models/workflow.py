from odoo import models, fields


class WorkflowActionRuleAccount(models.Model):
    _inherit = ['documents.workflow.rule']

    create_model = fields.Selection(
        selection_add=[
            ('l10n_edi_document.edi.document', "EDI Document")], ondelete={'l10n_edi_document.edi.document': 'cascade'})
