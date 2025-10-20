from odoo import api, fields, models
from odoo.exceptions import ValidationError

class PricingLine(models.Model):
    _name = 'pricing.line'
    _description = 'Pricing Line'

    crm_lead_proposal_id = fields.Many2one('crm.lead.proposal', ondelete='cascade')
    employee_id = fields.Many2one('hr.employee', string='Assigned Employee')
    hourly_cost = fields.Float(string='Employee Hourly Rate', compute='_compute_hourly_cost')
    planned_hours = fields.Integer(string='Estimated Hours')
    flight_cost = fields.Float(string='Travel Expense')
    night_cost = fields.Float(string='Hotel Cost')
    perdiem_cost = fields.Float(string='Daily Allowance')

    @api.constrains('employee_id')
    def _check_employee_id(self):
        for record in self:
            if record.employee_id and not record.employee_id.active:
                raise ValidationError('Any assigned employee must be active. (the employee you assigned is inactive)')
    
    @api.constrains('employee_id')
    def _check_hourly_cost(self):
        for record in self:
            if record.hourly_cost < 0:
                raise ValidationError('A pricing line\'s hourly_cost cannot be negative')
    
    @api.constrains('planned_hours')
    def _check_planned_hours(self):
        for record in self:
            if record.planned_hours < 0:
                raise ValidationError('A pricing line\'s planned_hours cannot be negative')
    
    @api.constrains('flight_cost')
    def _check_flight_cost(self):
        for record in self:
            if record.flight_cost < 0:
                raise ValidationError('A pricing line\'s flight_cost cannot be negative')
    
    @api.constrains('night_cost')
    def _check_night_cost(self):
        for record in self:
            if record.night_cost < 0:
                raise ValidationError('A pricing line\'s night_cost cannot be negative')
    
    @api.constrains('perdiem_cost')
    def _check_perdiem_cost(self):
        for record in self:
            if record.perdiem_cost < 0:
                raise ValidationError('A pricing line\'s perdiem_cost cannot be negative')

    @api.depends('employee_id.hourly_cost')
    def _compute_hourly_cost(self):
        for record in self:
            record.hourly_cost = record.employee_id.hourly_cost