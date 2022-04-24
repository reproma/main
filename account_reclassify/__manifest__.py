{
    "name": "Reclassify Journal Entries",
    "author": "Vauxoo",
    "summary": """Reclassify journal items without all the accounting workflow.
    """,
    "website": "http://www.vauxoo.com",
    "license": "LGPL-3",
    "category": "Vauxoo",
    "version": "14.0.1.0.1",
    "depends": [
        "account_budget",
        "account_accountant",
    ],
    "data": [
        "security/res_groups.xml",
        "wizard/account_reclassify_view.xml"
    ],
    "demo": [
    ],
    "test": [
    ],
    "qweb": ['static/src/xml/*.xml'],
    "auto_install": False,
    "price": 25,
    "installable": True,
}
