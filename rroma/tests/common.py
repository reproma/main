from odoo.tests import Form, TransactionCase


class RromaTransactionCase(TransactionCase):
    def setUp(self):
        super().setUp()
        self.product = self.env.ref('product.product_product_16')
        self.customer = self.env.ref('base.res_partner_2')
        self.helpdeskteam = self.env.ref('helpdesk.helpdesk_team1')
        self.maintenanceteam = self.env.ref('maintenance.equipment_team_maintenance')
        self.assigned = self.env.ref('base.user_demo')

    def create_equipment(self, customer, assigned):
        equipment_form = Form(self.env['maintenance.equipment'])
        equipment_form.name = 'Test Equipment'
        equipment_form.maintenance_team_id = self.maintenanceteam
        equipment_form.equipment_assign_to = 'customer'
        equipment_form.technician_user_id = assigned
        equipment_form.customer_id = customer
        equipment = equipment_form.save()
        return equipment

    def create_helpdesk(self, customer, assigned=None):
        assigned = assigned or self.assigned
        equipment = self.create_equipment(customer, assigned)
        helpdesk_form = Form(self.env['helpdesk.ticket'])
        helpdesk_form.name = 'Test Helpdesk Custom'
        helpdesk_form.team_id = self.helpdeskteam
        helpdesk_form.partner_id = customer
        helpdesk_form.user_id = assigned
        helpdesk_form.equipment_id = equipment
        helpdesk_order = helpdesk_form.save()
        return helpdesk_order

    def create_location(self, assigned):
        location_form = Form(self.env['stock.location'])
        location_form.name = assigned.name
        location_form.usage = 'internal'
        location_form.owner_id = assigned
        location = location_form.save()
        return location
