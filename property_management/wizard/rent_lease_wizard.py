# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import date, datetime
from odoo.tools import date_utils
import io
import json

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class RentLeaseWizard(models.TransientModel):
    """class for defining rent lease wizard for printing reports"""
    _name = 'rent.lease.wizard'
    _description = 'Rent Lease Wizard'

    name = fields.Char(string="Name")
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
    state = fields.Selection(string='Agreement State',
                             selection=[('draft', 'Draft'), ('confirmed', 'Confirmed'),
                                        ('closed', 'Closed'),
                                        ('returned', 'Returned'), ('expired', 'Expired')
                                        ])
    tenant_id = fields.Many2one('res.partner', string="Tenant")
    owner_id = fields.Many2one('res.partner', string="Owner")
    type = fields.Selection(selection=[('rent', 'Rent'), ('lease', 'Lease')])
    property_id = fields.Many2one('property.management.properties')

    @api.constrains('to_date')
    def check_from_date(self):
        """function to add validation for from and to dates"""
        for rec in self:
            if rec.from_date and rec.to_date and rec.from_date > rec.to_date:
                raise ValidationError(_("Invalid Dates"))

    def action_print_xlsx_report(self):
        """function for printing xlsx report"""
        if self.from_date and self.to_date and self.from_date > self.to_date:
            raise ValidationError('Start Date must be less than End Date')
        data = {
            'model': 'rent.lease.wizard',
            'name': self.name,
            'from_date': self.from_date,
            'to_date': self.to_date,
            'state': self.state,
            'tenant': self.tenant_id.name,
            'owner': self.owner_id.name,
            'type': self.type,
            'property': self.property_id.name,
            'date': date.today()
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'rent.lease.wizard',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Rent Lease Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        """function to get xlsx data"""
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        query = ""
        columns = ['order_reference', 'from_date', 'to_date', 'state', 'tenant', 'owner', 'type', 'property']
        repeating_details = f"DATE : {data['date']}\n"
        if data['from_date'] and data['to_date']:
            query += f" a.related_start_date > '{datetime.strptime(str(data['from_date']), '%Y-%m-%d')}' AND a.related_end_date < '{datetime.strptime(str(data['to_date']), '%Y-%m-%d')}' AND"
        elif data['from_date']:
            query += f" a.related_start_date > '{datetime.strptime(str(data['from_date']), '%Y-%m-%d')}' AND"
        elif data['to_date']:
            query += f" a.related_end_date < '{datetime.strptime(str(data['to_date']), '%Y-%m-%d')}' AND"
        if data['state']:
            columns.remove('state')
            repeating_details += f'STATE : {data["state"]} \n'
            query += f" a.related_state='{data['state']}' AND"
        if data['tenant']:
            columns.remove('tenant')
            repeating_details += f'TENANT : {data["tenant"]} \n'
            query += f" c.name='{data['tenant']}' AND"
        if data['owner']:
            columns.remove('owner')
            repeating_details += f'OWNER : {data["owner"]} \n'
            query += f" b.name='{data['owner']}' AND"
        if data['type']:
            columns.remove('type')
            repeating_details += f'TYPE : {data["type"]} \n'
            query += f" a.related_type='{data['type']}' AND"
        if data['property']:
            columns.remove('property')
            repeating_details += f'PROPERTY : {data["property"]} \n'
            query += f" d.name='{data['property']}' AND"
        final_query = f"WHERE {query.strip('AND').strip(' ')}" if query else ""
        self.env.cr.execute(
            f"SELECT a.related_type as type,a.related_state as agreement_state,a.related_start_date as "
            f"agreement_start_date,a.related_end_date as agreement_end_date,a.related_order_id as order_reference,"
            f"b.name as owner,c.name as tenant,d.name as property,a.related_order_id as order_reference FROM "
            f"property_order_lines as a INNER JOIN res_partner as b ON a.related_owner_id=b.id INNER JOIN res_partner "
            f"as c ON a.related_tenant_id=c.id INNER JOIN property_management_properties as d ON a.props_id=d.id "
            f"{final_query}")
        records = self.env.cr.fetchall()
        if records:
            data['rent_lease_records'] = records
        else:
            raise ValidationError(_("Record Does Not Exist !"))
        format_address = workbook.add_format({'align': 'left'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        column_head = workbook.add_format({'font_size': '12px', 'align': 'center', 'bold': True})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                     'U', 'V', 'W', 'X', 'Y', 'Z']
        sheet.merge_range('A2:D2', f'Rent Lease Report', head)
        for index, col in enumerate(columns):
            sheet.write(f'{alphabets[index]}4', col.capitalize().replace('_', ' '), column_head)
        sheet.set_column('A:F', 20)
        for index, rec in enumerate(data['rent_lease_records']):
            ind_from_date = columns.index('from_date')
            sheet.write(f'{alphabets[ind_from_date]}{index + 5}', str(rec[2].date()), txt)
            ind_to_date = columns.index('to_date')
            sheet.write(f'{alphabets[ind_to_date]}{index + 5}', str(rec[3].date()), txt)
            if not data['state']:
                ind_state = columns.index('state')
                sheet.write(f'{alphabets[ind_state]}{index + 5}', rec[1], txt)
            if not data['tenant']:
                ind_tenant = columns.index('tenant')
                sheet.write(f'{alphabets[ind_tenant]}{index + 5}', rec[6], txt)
            if not data['owner']:
                ind_owner = columns.index('owner')
                sheet.write(f'{alphabets[ind_owner]}{index + 5}', rec[5], txt)
            if not data['type']:
                ind_type = columns.index('type')
                sheet.write(f'{alphabets[ind_type]}{index + 5}', rec[0], txt)
            if not data['property']:
                ind_property = columns.index('property')
                sheet.write(f'{alphabets[ind_property]}{index + 5}', rec[7], txt)
            ind_order_reference = columns.index('order_reference')
            sheet.write(f'{alphabets[ind_order_reference]}{index + 5}', rec[8], txt)
        sheet.set_row(0, 60)
        sheet.set_row(1, 40)
        sheet.set_row(2, 60)
        sheet.merge_range('A1:B1',
                          f' {self.env.company.name} \n {self.env.company.street} \n {self.env.company.city} {self.env.company.zip} \n {self.env.company.country_id.name}',
                          format_address)
        sheet.merge_range('A3:B3', repeating_details, format_address)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

    def action_print_pdf_report(self):
        """function for printing pdf report"""
        data = {
            'model': 'rent.lease.wizard',
            'name': self.name,
            'from_date': self.from_date,
            'to_date': self.to_date,
            'state': self.state,
            'tenant': self.tenant_id.name,
            'owner': self.owner_id.name,
            'type': self.type,
            'property': self.property_id.name,
            'date': date.today()
        }
        return self.env.ref('property_management.action_report_property_rent_lease_management').report_action(None,
                                                                                                              data=data)
