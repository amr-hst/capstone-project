from odoo import fields, models

class PricingLine(models.Model):
    _name="pricing.line"

    crm_lead_proposal_id=fields.Many2one("crm.lead.proposal")
    employee_id=fields.Many2one("hr.employee", string="Assigned employee")
    hourly_cost=fields.Float(string="Employee hourly rate")
    planned_hours=fields.Integer(string="Estimated hours")
    flight_cost=fields.Float(string="Travel expenses")
    night_cost=fields.Float(string="Hotel costs")
    perdiem_cost=fields.Float(string="Daily allowances")