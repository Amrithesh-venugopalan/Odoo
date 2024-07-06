# -*- coding: utf-8 -*-

from odoo import fields, models


# -*- coding: utf-8 -*-


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    employee_level_id = fields.Many2one('employee.level', string='Employee Level')
    employee_salary = fields.Integer(related='employee_level_id.salary')
    highest_level = fields.Boolean(default=False)

    def action_promote_employee(self):
        all_levels = self.env['employee.level'].search([])
        current_emp_level_id = self.employee_level_id.id

        if self.employee_level_id:
            print('current emp id', current_emp_level_id)
            for index, level in enumerate(all_levels):
                if level.id == current_emp_level_id and index != len(all_levels) - 1:
                    print('in if ')
                    self.employee_level_id = all_levels[index + 1]
                    break
                elif current_emp_level_id == all_levels[-1].id:
                    print('in else')
                    self.highest_level = True
                    break
        else:
            self.employee_level_id = all_levels[0]
