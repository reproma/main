from odoo import models, fields, api, _
from collections import defaultdict


class AccountReclassify(models.TransientModel):
    _name = 'account.reclassify'
    _description = 'Reclassify journal entries'

    @api.model
    def default_get(self, default_fields):
        res = super(AccountReclassify, self).default_get(default_fields)
        res['invoice_ids'] = self._context.get('active_ids')
        res.update(self.get_docs(self._context.get('active_ids')))
        return res

    @api.model
    def get_docs(self, docs):
        invoice_ids = self.env['account.move'].search([
            ('id', 'in', docs), ('state', 'in', ('draft', 'posted', 'paid'))])
        result = defaultdict(list)
        for inv in invoice_ids:
            if ((inv.state == 'posted' and inv.invoice_payments_widget != 'false') or
                    (inv.state == 'paid' and inv.invoice_payments_widget == 'false')):
                continue
            if inv.type in ['out_invoice', 'out_refund']:
                result['%s_invoice_out_ids' % inv.state].append(inv.id)
                continue
            if inv.type in ['in_invoice', 'in_refund']:
                result['%s_invoice_in_ids' % inv.state].append(inv.id)
        return result

    date = fields.Date(
        help="This will change the accounting affectation date (if sale "
             "invoice this will not be set)")
    product_id = fields.Many2one(
        'product.product',
        help="If an vendor bill then the product will be forced in all lines.")
    account_id = fields.Many2one(
        'account.account',
        help="The account move lines for this list of bills will be set with "
             "this account, either on the income or the expense account "
             "(account set in lines on the invoices)")
    analytic_id = fields.Many2one(
        'account.analytic.account',
        groups='analytic.group_analytic_accounting',
        help="If set will force the assignation of this analytic tag to all "
             "expense and income account move lines in the invoice and fully "
             "re-generate the analytic lines."
    )
    analytic_tag_ids = fields.Many2many(
        'account.analytic.tag',
        groups='analytic.group_analytic_accounting',
        help="If set will force the assignation of this analytic tag to all "
             "expense and income account move lines in the invoice and fully "
             "re-generate the analytic lines."
    )
    comments = fields.Html(
        help="The text here will be attach to the message post to explain"
             "better why and how the change was done.")
    invoice_ids = fields.Many2many('account.move')
    paid_invoice_in_ids = fields.Many2many(
        'account.move', 'rel_invs_in_paid', 'in_paid_id', 'wiz_id')
    draft_invoice_in_ids = fields.Many2many(
        'account.move', 'rel_invs_in_draft', 'in_draft_id', 'wiz_id')
    posted_invoice_in_ids = fields.Many2many(
        'account.move', 'rel_invs_in_posted', 'in_posted_id', 'wiz_id')
    paid_invoice_out_ids = fields.Many2many(
        'account.move', 'rel_invs_out_paid', 'out_paid_id', 'wiz_id')
    draft_invoice_out_ids = fields.Many2many(
        'account.move', 'rel_invs_out_draft', 'out_draft_id', 'wiz_id')
    posted_invoice_out_ids = fields.Many2many(
        'account.move', 'rel_invs_out_posted', 'out_posted_id', 'wiz_id')
    show = fields.Boolean(help="Show documents that will be affected.")

    def reclassify(self):
        in_invoices = self.reclassify_in_invoices()
        out_invoices = self.reclassify_out_invoices()
        action = self.env.ref(
            'account_reclassify.action_all_partner_invoices').read()[0]
        domain = [('id', 'in', in_invoices.ids + out_invoices.ids)]
        if len(in_invoices.ids + out_invoices.ids) == 1:
            return {}
        action.update({'domain': domain})
        return action

    def reclassify_in_invoices(self):
        return self._reclassify_invoices()

    def reclassify_out_invoices(self):
        return self._reclassify_invoices(in_out='out')

    def _reclassify_invoices(self, in_out='in'):
        invoices = self.posted_invoice_in_ids + self.paid_invoice_in_ids
        if in_out == 'out':
            invoices = self.posted_invoice_out_ids + self.paid_invoice_out_ids
        # Date ca not be changed only if not sale document
        if self.date and in_out != 'out':
            invoices.write({'date': self.date})
        lines = invoices.mapped('invoice_line_ids')
        if lines and hasattr(lines[0], "is_anglo_saxon_line"):
            lines = lines.filtered(lambda x: not x.is_anglo_saxon_line)
        rfields = ['account_id', 'product_id',
                   'analytic_account_id', 'analytic_tag_ids']
        message = {}
        for line in lines:
            old_message = message.get(line.move_id.id, '')
            message[line.move_id.id] = _(
                "<b>Line reclassified from:</b> %s <br/>\n%s") % (str(line.read(rfields)), old_message)
            line.account_id = self.account_id or line.account_id
            line.product_id = self.product_id or line.product_id
            line.analytic_account_id = self.analytic_id or line.analytic_account_id
            line.analytic_tag_ids = self.analytic_tag_ids or line.analytic_tag_ids
            old_message = message.get(line.move_id.id, '')
            message[line.move_id.id] = _(
                "<b>Line reclassified to:</b> %s <br/>\n%s") % (str(line.read(rfields)), old_message)

        for move in invoices:
            self._reclassify_move(move)

        comments = ''
        if len(self.comments or '') > 11:
            comments = _("<b>Comments</b><br><br>%s") % self.comments
        for invoice in invoices:
            composed = "%s%s" % (comments, message.get(invoice.id, ''))
            invoice.message_post(body=composed)
        return invoices

    def _reclassify_move(self, move):
        if move.state == 'posted':
            move.button_cancel()
        move.date = self.date if self.date and move.journal_id.type != 'sale' \
            else move.date
        lines = move.line_ids.filtered(
            lambda l: l.account_id.user_type_id.type not in
            ['payable', 'receivable'] and not l.tax_line_id)
        for line in lines:
            acc = self.account_id if self.account_id else line.account_id
            analytic = self.analytic_id if self.analytic_id \
                else line.analytic_account_id
            tags = self.analytic_tag_ids if self.analytic_tag_ids \
                else line.analytic_tag_ids
            line.write({
                'account_id': acc.id,
                'analytic_account_id': analytic.id,
                'analytic_tag_ids': [(6, 0, tags.ids)],
            })
        if move.state != 'posted':
            move.post()
