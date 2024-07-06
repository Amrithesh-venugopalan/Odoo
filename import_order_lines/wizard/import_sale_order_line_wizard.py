# -*- coding: utf-8 -*-

from odoo import models, fields, _
import openpyxl
import base64
from io import BytesIO
from odoo.exceptions import UserError


class ImportSaleOrderLineWizard(models.TransientModel):
    """import sale order lines from xlsx files"""
    _name = "import.sale.order.line.wizard"
    file = fields.Binary(string="File", required=True)
    sale_order_id = fields.Many2one('sale.order')

    def action_import_order_line(self):
        """function for importing records from xlsx file to sale order"""
        try:
            wb = openpyxl.load_workbook(
                filename=BytesIO(base64.b64decode(self.file)), read_only=True
            )
            ws = wb.active
            for record in ws.iter_rows(min_row=2, max_row=None, min_col=None,
                                       max_col=None, values_only=True):

                all_product_names = self.env['product.template'].search([]).mapped('name')
                all_category_names = self.env['uom.category'].search([]).mapped('name')
                all_uom_names = self.env['uom.uom'].search([]).mapped('name')

                if record[5] and record[5] not in all_category_names:
                    self.env['uom.category'].create({
                        'name': record[5]
                    })
                if record[2] and record[2] not in all_uom_names:
                    self.env['uom.uom'].create({
                        'name': record[2],
                        'category_id': self.env['uom.category'].search([('name', '=', record[5])]).id,
                        'uom_type': 'smaller' if 'reference' in self.env['uom.category'].search(
                            [('name', '=', record[5])]).uom_ids.mapped('uom_type') else 'reference'
                    })
                if record[0] in all_product_names:
                    product_record = self.env['product.product'].search([('name', '=', record[0])])[0]
                else:
                    product_uom_id = self.env['uom.uom'].search([('name', '=', record[2])])
                    product_record = self.env['product.product'].create({'name': record[0], 'list_price': record[4],
                                                                         'uom_id': product_uom_id.id if product_uom_id else 1,
                                                                         'uom_po_id': product_uom_id.id if product_uom_id else 1})
                sale_order_lines = [(fields.Command.create({
                    'name': record[3] if record[3] else 'item',
                    'order_id': self.sale_order_id.id,
                    'price_unit': record[4] if record[4] else product_record.list_price,
                    'product_uom_qty': record[1] if record[1] else 1,
                    'product_id': product_record.id,
                    'product_uom': self.env['uom.uom'].search([('name', '=', record[2])]).id if record[
                        2] else product_record.uom_id.id,
                }))]
                self.sale_order_id.update({
                    'order_line': sale_order_lines})
        except:
            raise UserError(_('Please insert a valid file'))


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_import_sale_order_lines(self):
        return {
            'name': 'Import Sale Order Lines',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'import.sale.order.line.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
