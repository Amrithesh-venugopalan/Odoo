# -*- coding: utf-8 -*-

from odoo import fields, models


class EmployeeLevel(models.Model):
    _name = 'employee.level'
    _description = 'Employee Level'

    sequence = fields.Integer(string='Sequence')
    name = fields.Char(string="Employee Level")
    salary = fields.Integer(string="Employee Salary")

