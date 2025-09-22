from odoo import api, fields, models
from odoo.exceptions import ValidationError

class HSTLead(models.Model):
    _inherit='crm.lead'
    _sql_constraints=[
        ('unique_project_id', 'unique(project_id)', 'Each CRM lead can only have one project, and vice versa.'),
    ]
    
    #CRM Project Pricing Tools fields:
    project_id=fields.Many2one('project.project')
    project_manager_id=fields.Many2one('hr.employee')
    selected_pricing=fields.Selection([('standard', 'Standard Margins'),
                                ('competitive', 'Competitive Margins'),
                                ('high', 'High Margins')])
    selected_final_price=fields.Float()
    crm_lead_proposal_ids=fields.One2many('crm.lead.proposal', 'crm_lead_id')

    first_proposal_id=fields.Many2one('crm.lead.proposal', compute='_compute_proposal_ids')
    second_proposal_id=fields.Many2one('crm.lead.proposal', compute='_compute_proposal_ids')
    third_proposal_id=fields.Many2one('crm.lead.proposal', compute='_compute_proposal_ids')

    first_direct_price_ids=fields.One2many(related='first_proposal_id.direct_cost_ids', readonly=False)
    second_direct_price_ids=fields.One2many(related='second_proposal_id.direct_cost_ids', readonly=False)
    third_direct_price_ids=fields.One2many(related='third_proposal_id.direct_cost_ids', readonly=False)

    first_pricing_line_ids=fields.One2many(related='first_proposal_id.pricing_line_ids', readonly=False)
    second_pricing_line_ids=fields.One2many(related='second_proposal_id.pricing_line_ids', readonly=False)
    third_pricing_line_ids=fields.One2many(related='third_proposal_id.pricing_line_ids', readonly=False)

    first_overhead_margin=fields.Float(related='first_proposal_id.overhead_margin', readonly=False)
    second_overhead_margin=fields.Float(related='second_proposal_id.overhead_margin', readonly=False)
    third_overhead_margin=fields.Float(related='third_proposal_id.overhead_margin', readonly=False)
    
    first_profit_margin=fields.Float(related='first_proposal_id.profit_margin', readonly=False)
    second_profit_margin=fields.Float(related='second_proposal_id.profit_margin', readonly=False)
    third_profit_margin=fields.Float(related='third_proposal_id.profit_margin', readonly=False)

    first_total_direct_cost=fields.Float(related='first_proposal_id.total_direct_cost')
    second_total_direct_cost=fields.Float(related='second_proposal_id.total_direct_cost')
    third_total_direct_cost=fields.Float(related='third_proposal_id.total_direct_cost')

    first_total_pricing_line=fields.Float(related='first_proposal_id.total_pricing_line')
    second_total_pricing_line=fields.Float(related='second_proposal_id.total_pricing_line')
    third_total_pricing_line=fields.Float(related='third_proposal_id.total_pricing_line')


    @api.constrains('project_manager_id')
    def _check_project_manager_id(self):
        for record in self:
            if record.project_manager_id and not record.project_manager_id.active:
                raise ValidationError('The project manager must be an active employee!')
    
    @api.depends('crm_lead_proposal_ids.proposal_number')
    def _compute_proposal_ids(self):
        for record in self:
            record.first_proposal_id=record.crm_lead_proposal_ids.filtered(lambda p: p.proposal_number == 'first')[:1] or False
            record.second_proposal_id=record.crm_lead_proposal_ids.filtered(lambda p: p.proposal_number == 'second')[:1] or False
            record.third_proposal_id=record.crm_lead_proposal_ids.filtered(lambda p: p.proposal_number == 'third')[:1] or False
    
    def action_create_first_proposal(self):
        for record in self:
            record.env['crm.lead.proposal'].create([{'name': record.name + '\'s first proposal',
                                                'crm_lead_id': record.id,
                                                'proposal_number': 'first'}])
    
    def action_create_second_proposal(self):
        for record in self:
            record.env['crm.lead.proposal'].create([{'name': record.name + '\'s second proposal',
                                                'crm_lead_id': record.id,
                                                'proposal_number': 'second'}])
    
    def action_create_third_proposal(self):
        for record in self:
            record.env['crm.lead.proposal'].create([{'name': record.name + '\'s third proposal',
                                                'crm_lead_id': record.id,
                                                'proposal_number': 'third'}])