import time
from odoo.tests.common import Form, TransactionCase


class TestReclassify(TransactionCase):

    def setUp(self):
        super(TestReclassify, self).setUp()
        self.company = self.env.ref("base.main_company")
        self.misc_journal = self.env['account.journal'].create({
            'company_id': self.company.id,
            'type': 'general',
            'code': 'MISC',
            'name': 'MISC',
        })
        self.sale_journal = self.env['account.journal'].create({
            'company_id': self.company.id,
            'type': 'sale',
            'code': 'SALE',
            'name': 'SALE',
        })
        self.user = self.env.ref("base.user_demo")
        self.partner = self.env.ref("base.res_partner_12")
        self.date = time.strftime('%Y-%m')+'-01'
        self.product_1 = self.env.ref("product.consu_delivery_02")
        self.product_2 = self.env.ref("product.consu_delivery_03")
        self.origin_account = self.env['account.account'].create({
            'name': 'Test Account Origin',
            'code': 'CodeOrigin',
            'user_type_id': self.env.ref(
                'account.data_account_type_other_income').id,
        })
        move_form = Form(self.env["account.move"].with_context(default_type='out_invoice'))
        move_form.invoice_date = self.date
        move_form.partner_id = self.partner
        with move_form.invoice_line_ids.new() as line:
            line.product_id = self.env.ref('product.product_product_4')
            line.quantity = 1.0
            line.price_unit = 100.0
            line.name = 'product that cost 100'
            line.account_id = self.origin_account
        self.invoice = move_form.save()
        self.journal = self.invoice.journal_id
        self.destiny_account = self.env['account.account'].create({
            'name': 'Test Account Destiny',
            'code': 'CodeDestiny',
            'user_type_id': self.env.ref(
                'account.data_account_type_other_income').id,
        })
        self.wizard = self.env['account.reclassify']

    def test_10_reclassify(self):
        """Basic reclassification wizard being tested"""
        # self.journal.write({'update_posted': True})
        self.invoice.action_post()
        wizard = self.wizard.with_context({
            'active_ids': [self.invoice.id]
        }).create({'account_id': self.destiny_account.id})

        wizard.reclassify()

        self.assertIn(
            self.destiny_account,
            self.invoice.invoice_line_ids.mapped('account_id'),
            "The new account was not assigned to the invoice.")

        # New invoice to check it multi
        invoice2 = self.invoice.copy()
        invoice2.action_post()

        wizard = self.wizard.with_context({
            'active_ids': [self.invoice.id, invoice2.id]
        }).create({'account_id': self.destiny_account.id})
        wizard.reclassify()

        self.assertIn(
            self.destiny_account,
            invoice2.invoice_line_ids.mapped('account_id'),
            "The new account was not assigned to the invoice.")

        # Check in_invoice.
        invoice3 = self.invoice.copy()
        invoice3.write({'type': 'in_invoice'})
        invoice3.action_post()

        wizard = self.wizard.with_context({
            'active_ids': [invoice3.id]
        }).create({
            'account_id': self.destiny_account.id,
            'date': self.date,
            'comments': 'Just checking',
        })
        wizard.reclassify()

        self.assertIn(
            self.destiny_account,
            invoice3.invoice_line_ids.mapped('account_id'),
            "The new account was not assigned to the invoice.")
