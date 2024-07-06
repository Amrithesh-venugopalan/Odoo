# -*- coding: utf-8 -*-

from odoo import models, api, _
from datetime import datetime
from odoo.exceptions import ValidationError


class RentLeaseReport(models.AbstractModel):
    """Abstract model class for passing in data to report template"""
    _name = 'report.property_management.report_management'
    _description = 'Rent Lease Report'

    @api.model
    def _get_report_values(self, docids, data):
        """function to pass in data to the template"""
        query = ""
        if data['from_date'] and data['to_date']:
            query += (f" a.related_start_date > '{datetime.strptime(str(data['from_date']), '%Y-%m-%d')}' AND "
                      f"a.related_end_date < '{datetime.strptime(str(data['to_date']), '%Y-%m-%d')}' AND")
        elif data['from_date']:
            query += f" a.related_start_date > '{datetime.strptime(str(data['from_date']), '%Y-%m-%d')}' AND"
        elif data['to_date']:
            query += f" a.related_end_date < '{datetime.strptime(str(data['to_date']), '%Y-%m-%d')}' AND"
        if data['state']:
            query += f" a.related_state='{data['state']}' AND"
        if data['tenant']:
            query += f" c.name='{data['tenant']}' AND"
        if data['owner']:
            query += f" b.name='{data['owner']}' AND"
        if data['type']:
            query += f" a.related_type='{data['type']}' AND"
        if data['property']:
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
            return {
                'data': data,
            }
        else:
            raise ValidationError(_("Record Does Not Exist !"))
