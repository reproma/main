# Copyright 2020 Vauxoo
# License AGPL-3 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Instance creator for rroma',
    'summary': '''
    Instance creator for rroma. This is the app.
    ''',
    'author': 'Vauxoo',
    'website': 'https://www.vauxoo.com',
    'license': 'AGPL-3',
    'category': 'Installer',
    'version': '14.0.1.0.2',
    'depends': [
        'account_accountant',
        'crm',
        'helpdesk',
        'hr_holidays',
        'hr_recruitment',
        #'helpdesk_fsm',
        'l10n_cr_currency_rate_live',
        'l10n_cr_edi',
        'l10n_cr_edi_qr',
        'l10n_cr_edi_document',
        #'maintenance',
        'mrp',
        'purchase',
        #'repair',
        'stock_by_warehouse',
        'stock_no_negative',
        'stock_landed_costs',
    ],
    'data': [
        # data
        'data/res_company_data.xml',
        'data/settings.xml',
        'security/res_groups.xml',
        'data/mail_data.xml',
        'data/helpdesk_data.xml',
        'data/ir_actions_server.xml',
        # views
        #'views/maintenance_views.xml',
        #'views/helpdesk_views.xml',
        #'views/project_task_views.xml',
        'views/purchase_views.xml',
        #'views/stock_location_views.xml',
        #'views/repair_views.xml',
        'views/account_invoice.xml',
        'views/account_move.xml',
        'views/product_template_views.xml',
        'views/stock_menu_views.xml',
        'views/account_payment_view.xml',
        # reports
        'reports/purchase_quotation_templates.xml',
        'reports/purchase_order_templates.xml',
        'reports/sale_report_templates.xml',
        'reports/report_invoice.xml',
        'reports/report_payment_receipt_templates.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
