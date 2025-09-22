from odoo import fields, models

class PricingLine(models.Model):
    _name='pricing.line'

    crm_lead_proposal_id=fields.Many2one('crm.lead.proposal', ondelete='cascade')
    employee_id=fields.Many2one('hr.employee', string='Assigned Employee')
    hourly_cost=fields.Float(string='Employee Hourly Rate')
    planned_hours=fields.Integer(string='Estimated Hours')
    flight_cost=fields.Float(string='Travel Expense')
    night_cost=fields.Float(string='Hotel Cost')
    perdiem_cost=fields.Float(string='Daily Allowance')