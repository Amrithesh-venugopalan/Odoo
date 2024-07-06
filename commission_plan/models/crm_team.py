from odoo import fields, models


class Team(models.Model):
    _inherit = 'crm.team'

    commission_plan_id = fields.Many2one('crm.commission', string="Commission Plan")
    all_team_commission_ids = fields.One2many('commission.team.amount.lines', 'commission_team_amount_id', string="All commission")


class CommissionTeamAmountLines(models.Model):
    _name = 'commission.team.amount.lines'

    commission_team_amount_id = fields.Many2one('res.users')
    sale_team_order_id = fields.Many2one('sale.order', 'Sale Order')
    team_commission_amount = fields.Float(string='Amount')
