from odoo import api, fields, models
from odoo.exceptions import ValidationError

class CRMProposals(models.Model):
    _name = 'crm.lead.proposal'
    _description = 'CRM Lead Proposal'
    _sql_constraints = [
        ('unique_lead_proposal', 'unique(crm_lead_id, proposal_number)', 'Ensures there are no duplicates amongst the pairs of the \'crm_lead_id\' & \'proposal_number\' fields, meaning there can only be three proposals per lead.')
    ]

    name = fields.Char(required=True)
    crm_lead_id = fields.Many2one('crm.lead', required=True, ondelete='cascade')
    proposal_number = fields.Selection([('first', 'First'),
                                ('second', 'Second'),
                                ('third', 'Third')],
                                required=True)
    direct_cost_ids = fields.One2many('direct.cost', 'crm_lead_proposal_id')
    pricing_line_ids = fields.One2many('pricing.line', 'crm_lead_proposal_id')
    overhead_fixed = fields.Boolean(string='Is overhead fixed?')
    overhead_margin_fixed = fields.Float()
    overhead_margin_percentage = fields.Float()
    profit_margin = fields.Float()
    total_direct_cost = fields.Float(compute='_compute_total_direct_cost')
    total_pricing_line = fields.Float(compute='_compute_total_pricing_line')
    final_project_cost = fields.Float(compute='_compute_final_project_cost')
    submitted = fields.Boolean()
    
    # @api.constrains('overhead_fixed', 'overhead_margin_fixed', 'overhead_margin_percentage')
    # def _check_overhead_margin(self):
    #     for record in self:
    #         if record.overhead_fixed == True and record.overhead_margin_fixed < 0:
    #             raise ValidationError('A proposal\'s overhead_margin_fixed cannot be negative'+('True' if record.overhead_fixed else 'False')+', '+('True' if record.env['crm.lead.proposal'].search([('id','=',record.id)]).overhead_fixed else 'False'))
    #         if not record.overhead_fixed and record.overhead_margin_percentage < 0:
    #             raise ValidationError('A proposal\'s overhead_margin_percentage cannot be negative')
    
    @api.constrains('overhead_margin_fixed', 'overhead_margin_percentage')
    def _check_overhead_margin(self):
        for record in self:
            if record.overhead_margin_fixed < 0:
                raise ValidationError('A proposal\'s overhead_margin_fixed cannot be negative')
            if record.overhead_margin_percentage < 0:
                raise ValidationError('A proposal\'s overhead_margin_percentage cannot be negative')
    
    @api.constrains('profit_margin')
    def _check_profit_margin(self):
        for record in self:
            if record.profit_margin < 0:
                raise ValidationError('A proposal\'s profit_margin cannot be negative')

    @api.depends('direct_cost_ids.amount')
    def _compute_total_direct_cost(self):
        for record in self:
            record.total_direct_cost = sum(line.amount for line in record.direct_cost_ids)
    
    @api.depends('pricing_line_ids.hourly_cost', 'pricing_line_ids.planned_hours', 'pricing_line_ids.flight_cost', 'pricing_line_ids.night_cost', 'pricing_line_ids.perdiem_cost', 'overhead_fixed', 'overhead_margin_fixed', 'overhead_margin_percentage')
    def _compute_total_pricing_line(self):
        for record in self:
            if record.overhead_fixed:
                record.total_pricing_line = sum((line.hourly_cost*line.planned_hours)+line.flight_cost+line.night_cost+line.perdiem_cost for line in record.pricing_line_ids)+record.overhead_margin_fixed
            else:
                record.total_pricing_line = sum((line.hourly_cost*line.planned_hours)+line.flight_cost+line.night_cost+line.perdiem_cost for line in record.pricing_line_ids)*(1+record.overhead_margin_percentage)
    
    @api.depends('total_pricing_line', 'total_direct_cost', 'profit_margin')
    def _compute_final_project_cost(self):
        for record in self:
            record.final_project_cost = (record.total_pricing_line+record.total_direct_cost)*(1+record.profit_margin)
    
    def action_submit(self):
        for record in self:
            record.submitted = True
    
    def action_withdraw(self):
        for record in self:
            record.submitted = False