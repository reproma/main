# -*- coding: utf-8 -*-
{
    'name': 'Odoo Purchase Order templates',
    'version': '14.0.0.1',
    'summary': 'Report Templates for RFQ/PO/Purchases',
    'category': 'Tools',
    'description': """
		Customize customize Purchase Order reportwith templates.
		
    """,
    'author': 'CYSFuturo',
    'website': 'https://www.cysfuturo.com',
    'depends': ['purchase',],
    'data': [
        "res_company.xml",
        "purchase_report/classic_report_purchaseorder.xml",
        "purchase_report/classic_report_purchasequotation.xml",
        "purchase_report/fancy_report_purchaseorder.xml",
        "purchase_report/fancy_report_purchasequotation.xml",
        "purchase_report/modern_report_purchaseorder.xml",
        "purchase_report/modern_report_purchasequotation.xml",
        "purchase_report/odoo_standard_report_purchaseorder.xml",
        "purchase_report/odoo_standard_report_purchasequotation.xml",
    ],
    'installable': True,
    'auto_install': False,
}
