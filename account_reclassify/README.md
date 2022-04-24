.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
      :alt: License: LGPL-3

Reclassify Journal Entries from Invoices.
=========================================

This module reclassify journal items without all the accounting workflow. 

**Problem:** Once an invoice is done there is a lot of manual steps to reclassify 
the account move lines either from an analytic of financial stand
point.

**Solution:** Following the current accounting secured workflow, ask for the
minimal information required to set the proper accounts in an invoice analytic
tags or analytic accounts.

Features of module
------------------

    - Change accounts, analytic accounts, products and analytic tag on the invoice lines.
    - Change Invoice Date (only available for Vendor Bills).
    - Change multiple invoices at once.

Which users should use it
-------------------------

    - Accountants
    - Accounting assistants
    - Related users

Installation
------------

Simple install the module.

Usage
-----

- **1. Go to Accounting -> Invoices**

    .. image:: account_reclassify/static/description/menu_invoices.png
        :alt: Invoices

- **2. In Invoices list, select the invoices you want to modify**

    .. image:: account_reclassify/static/description/list_invoices.png
        :alt: Invoices List

- **3. Press Actions -> Reclassify Move Lines**

    .. image:: account_reclassify/static/description/menu_reclassify.png
        :alt: Reclassify Move Lines

- **4. In Wizard, put the values you want to set**

    .. image:: account_reclassify/static/description/view_wizard.png
        :alt: Wizard

- **5. Press Execute**

    .. image:: account_reclassify/static/description/button_execute.png
        :alt: Button Execute

**Invoice lines before reclassifying:**

    .. image:: account_reclassify/static/description/before_invoice.png
        :alt: Invoice before reclassifying

**Invoice lines after reclassifying:**

    .. image:: account_reclassify/static/description/after_invoice.png
        :alt: Invoice after reclassifying

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.vauxoo.com/runbot/133/13.0

Credits
=======

This module was created by Vauxoo S.A. de C.V.

Contributors
------------

* Nhomar Hernandez <nhomar@vauxoo.com> (planner/developer)
* Hugo Adan <hugo@vauxoo.com> (developer)
* Luis Escobar <lescobar@vauxoo.com> (developer)

Maintainer
==========

.. image:: http://www.vauxoo.com/logo.png
   :alt: Vauxoo, S.A. de C.V.
   :target: http://www.vauxoo.com

This module is maintained by Vauxoo, S.A. de C.V.
