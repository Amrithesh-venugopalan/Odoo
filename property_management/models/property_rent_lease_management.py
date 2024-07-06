# -*- coding: utf-8 -*-

from odoo import api, fields, models, Command, _
from datetime import datetime
from odoo.exceptions import ValidationError


class PropertyRentLeaseManagement(models.Model):
    """class for creating rent lease records for properties"""

    _name = 'property.rent.lease.management'
    _description = 'Property Rent and Lease Management'
    _inherit = ['mail.thread']
    name = fields.Char(string='Order Reference',
                       readonly=True, default='New')
    total_days = fields.Integer(string='Duration in days', compute='_compute_total_days')
    rent_lease_amount = fields.Float(string='Rent/Lease Amount', compute='_compute_rent_lease_amount', store=True)
    current_date = fields.Date(default=datetime.today())
    agreement_start_date = fields.Datetime(string='Start Date')
    agreement_end_date = fields.Datetime(string='End Date')
    agreement_type = fields.Selection(selection=[('rent', 'Rent'), ('lease', 'Lease')], required=True)
    agreement_state = fields.Selection(string='Agreement State', tracking=True, required=True,
                                       selection=[('draft', 'Draft'), ('confirmed', 'Confirmed'),
                                                  ('closed', 'Closed'),
                                                  ('returned', 'Returned'), ('expired', 'Expired')
                                                  ],
                                       default='draft')
    show_invoice_button = fields.Boolean(default=False)
    tenant_id = fields.Many2one('res.partner', string='Tenant', copy=False, required=True)
    tenant_currency_id = fields.Many2one('res.currency', related='tenant_id.currency_id')
    company_id = fields.Many2one('res.company', string='Company', required=True, index=True,
                                 default=lambda self: self.env.company, readonly=True)
    property_ids = fields.One2many('property.order.lines', 'rent_lease_id', string="Properties")
    invoice_record_count = fields.Integer(compute="_compute_invoice_record_count")
    invoice_payment_state = fields.Selection(selection=[('not_paid', 'Not Paid'),
                                                        ('in_payment', 'In Payment'),
                                                        ('paid', 'Paid'),
                                                        ('partial', 'Partial'), ('reversed', 'Reversed')
                                                        ], compute="_compute_invoice_payment_state")
    previous_order_line_ids = fields.Many2many('property.management.properties',
                                               relation='previous_order_line_ids_table',
                                               string='previous order line ids')
    manager_agreement_approval = fields.Boolean(default=False)
    confirmation_request = fields.Boolean(default=False)
    show_confirm_button = fields.Boolean(compute="_compute_show_confirm_button")

    def _compute_show_confirm_button(self):
        """function to show confirm button based on security groups"""
        for rec in self:
            if rec.env.user.has_group('property_management.group_property_manager'):
                rec.show_confirm_button = True
            else:
                rec.show_confirm_button = False

    @api.depends('agreement_type', 'property_ids')
    def _compute_rent_lease_amount(self):
        """function to compute rent and lease amount for multiple properties"""
        for rec in self:
            total_rent_amount = 0
            total_lease_amount = 0
            for record in self.property_ids:
                total_lease_amount += record.prop_lease_amount
                total_rent_amount += record.prop_rent_amount
            if rec.agreement_type == 'rent':
                rec.rent_lease_amount = total_rent_amount
            else:
                rec.rent_lease_amount = total_lease_amount

    @api.depends('agreement_start_date', 'agreement_end_date')
    def _compute_total_days(self):
        """function to compute agreement period in days"""
        for rec in self:
            rec.total_days = 0
            if rec.agreement_start_date and rec.agreement_end_date:
                date_one = datetime.strptime(str(rec.agreement_start_date.date()), '%Y-%m-%d')
                date_two = datetime.strptime(str(rec.agreement_end_date.date()), '%Y-%m-%d')
                date_three = date_two - date_one
                rec.total_days = date_three.days

    def _compute_invoice_record_count(self):
        """function to compute the number of invoices for a particular record"""
        for rec in self:
            rec.invoice_record_count = rec.env['account.move'].search_count(
                [('related_agreement_id', '=', rec.id)]
            )

    def _compute_invoice_payment_state(self):
        """function to set current invoice payment state"""
        for rec in self:
            if rec.env['account.move'].search(
                    [('related_agreement_id', '=', rec.id)]):
                rec.invoice_payment_state = rec.env['account.move'].search(
                    [('related_agreement_id', '=', rec.id)]).payment_state
            else:
                rec.invoice_payment_state = rec.invoice_payment_state

    @api.onchange('property_ids')
    def _onchange_property_ids(self):
        """function to show invoice button"""
        if self.agreement_state != 'draft':
            self.show_invoice_button = True

    @api.onchange('agreement_end_date')
    def _onchange_agreement_end_date(self):
        """function to automatically set expiration state for records"""
        if self.agreement_state == 'confirmed':
            current_date = datetime.today()
            end_date = self.agreement_end_date
            if current_date > end_date:
                self.action_orders_expire()

    @api.model
    def create(self, vals):
        """function to create sequence number for record"""
        vals['name'] = self.env['ir.sequence'].next_by_code('property.rent.lease.management')
        return super(PropertyRentLeaseManagement, self).create(vals)

    @api.ondelete(at_uninstall=False)
    def _change_property_state(self):
        """function to set property back to draft stage on delete from property order lines"""
        for rec in self.property_ids:
            self.env['property.management.properties'].browse(rec.id).property_state = 'draft'

    def action_orders_confirm(self):
        """function to confirm agreement after checking requirements"""
        if self.env['ir.attachment'].search([('res_model', '=', self._name), ('res_id', '=', self._ids)]):
            for rec in self.env['property.management.properties'].search(
                    [('id', 'in', self.previous_order_line_ids.ids)]):
                rec.write({'property_state': 'draft'})
            self.previous_order_line_ids = [fields.Command.clear()]
            for rec in self.property_ids:
                self.previous_order_line_ids = [fields.Command.link(rec.props_id.id)]
            for rec in self.env['property.management.properties'].search(
                    [('id', 'in', [rec.props_id.id for rec in self.property_ids])]):
                rec.property_state = 'rented' if self.agreement_type == 'rent' else 'leased'
            self.agreement_state = 'confirmed'
            self.show_invoice_button = True
            if self.tenant_id.email:
                template = self.env.ref('property_management.property_mail_template')
                template.send_mail(self.id, force_send=True)
        else:
            raise ValidationError("Add an attachment")

    def action_orders_close(self):
        """function to close the agreement"""
        self.agreement_state = 'closed'
        if self.tenant_id.email:
            template = self.env.ref('property_management.property_mail_template')
            template.send_mail(self.id, force_send=True)

    def action_orders_return(self):
        """function to return the agreement"""
        self.agreement_state = 'returned'

    def action_orders_expire(self):
        """function to set agreement as expired"""
        self.agreement_state = 'expired'
        self.show_invoice_button = False
        if self.tenant_id.email:
            template = self.env.ref('property_management.property_mail_template')
            template.send_mail(self.id, force_send=True)

    def action_orders_draft(self):
        """function to set agreement to draft"""
        self.agreement_state = 'draft'
        self.show_invoice_button = False

    def action_confirmation_request(self):
        """function to set confirmation request"""
        self.confirmation_request = True

    def action_manager_agreement_approval(self):
        """function to set manager agreement approval"""
        self.manager_agreement_approval = True

    def display_chatter_message(self, message_body=''):
        """function to display chatter message"""
        for rec in self:
            rec.message_post(body=message_body)

    def create_property_invoice(self):
        """function to create related record invoice"""
        self.show_invoice_button = False
        if self.env['account.move'].search([('related_agreement_id', '=', self.id)]):
            self.env['account.move'].search([('related_agreement_id', '=', self.id)]).update({
                'invoice_line_ids': [(fields.Command.clear())]
            })
            self.env['account.move'].search([('related_agreement_id', '=', self.id)]).write(
                {'invoice_line_ids': [Command.create({
                    'price_unit': rec.prop_rent_amount if self.agreement_type == 'rent' else rec.prop_lease_amount,
                    'name': self.env['property.management.properties'].search([('id', '=', rec.props_id.id)]).name,
                }) for rec in self.property_ids]})
            account_id = self.env['account.move'].search([('related_agreement_id', '=', self.id)])
        else:
            account_id = self.env['account.move'].create([{
                'move_type': 'out_invoice',
                'partner_id': self.tenant_id.id,
                'date': self.current_date,
                'related_agreement_id': self.id,
                'invoice_date': self.current_date,
                'invoice_line_ids': [Command.create({
                    'price_unit': rec.prop_rent_amount if self.agreement_type == 'rent' else rec.prop_lease_amount,
                    'name': self.env['property.management.properties'].search([('id', '=', rec.props_id.id)]).name,
                }) for rec in self.property_ids]
            }])
        return {
            'name': _('Draft Invoices'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form,tree',
            'views': [(False, 'form')],
            'res_model': 'account.move',
            'res_id': account_id.id,
            'domain': [],
        }

    def get_invoice_record(self):
        """function to display related invoice"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [('related_agreement_id', '=', self.id)],
            'context': "{'create': False}"
        }

    def action_send_mail(self):
        """functon to send payment remainder mail to tenant"""
        for rec in self.env['property.rent.lease.management'].search([]):
            if rec.agreement_state == 'confirmed':
                current_date = datetime.today()
                end_date = rec.agreement_end_date
                if current_date > end_date:
                    rec.action_orders_expire()
                elif current_date.date() == end_date.date():
                    template = self.env.ref('property_management.payment_remainder_mail_template')
                    template.send_mail(rec.id, force_send=True)


class PropertyOrderLines(models.Model):
    """class for defining different property order lines in rent lease record"""
    _name = 'property.order.lines'
    _description = 'Property Order Lines'

    props_id = fields.Many2one('property.management.properties', string="Properties",
                               domain="[('property_state', '=', 'draft')]")
    prop_rent_amount = fields.Float(string="Rent Amount", related='props_id.rent', readonly=False)
    prop_lease_amount = fields.Float(string='Lease Amount', related='props_id.legal_amount', readonly=False)
    rent_lease_id = fields.Many2one('property.rent.lease.management')
    address_country_id = fields.Many2one('res.country', string='Country', required=True,
                                         related='props_id.address_country_id')
    related_order_id = fields.Char(related='rent_lease_id.name', store=True)
    related_start_date = fields.Datetime(related='rent_lease_id.agreement_start_date', store=True)
    related_end_date = fields.Datetime(related='rent_lease_id.agreement_end_date', store=True)
    related_state = fields.Selection(related='rent_lease_id.agreement_state', store=True)
    related_type = fields.Selection(related='rent_lease_id.agreement_type', store=True)
    related_owner_id = fields.Many2one('res.partner', related='props_id.property_owner_id', store=True)
    related_tenant_id = fields.Many2one('res.partner', related='rent_lease_id.tenant_id', store=True)
