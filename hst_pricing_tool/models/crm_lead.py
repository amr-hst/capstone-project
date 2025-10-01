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
    selected_final_price=fields.Float(compute='_compute_selected_final_price')
    crm_lead_proposal_ids=fields.One2many('crm.lead.proposal', 'crm_lead_id')
    approved_proposal_id=fields.Many2one('crm.lead.proposal')
    stage_name=fields.Char(related='stage_id.name')

    first_proposal_id=fields.Many2one('crm.lead.proposal', compute='_compute_proposal_ids', store=True, index=True)
    second_proposal_id=fields.Many2one('crm.lead.proposal', compute='_compute_proposal_ids', store=True, index=True)
    third_proposal_id=fields.Many2one('crm.lead.proposal', compute='_compute_proposal_ids', store=True, index=True)

    first_direct_cost_ids=fields.One2many(related='first_proposal_id.direct_cost_ids', readonly=False)
    second_direct_cost_ids=fields.One2many(related='second_proposal_id.direct_cost_ids', readonly=False)
    third_direct_cost_ids=fields.One2many(related='third_proposal_id.direct_cost_ids', readonly=False)

    first_pricing_line_ids=fields.One2many(related='first_proposal_id.pricing_line_ids', readonly=False)
    second_pricing_line_ids=fields.One2many(related='second_proposal_id.pricing_line_ids', readonly=False)
    third_pricing_line_ids=fields.One2many(related='third_proposal_id.pricing_line_ids', readonly=False)

    first_overhead_fixed=fields.Boolean(related='first_proposal_id.overhead_fixed', readonly=False, store=True)
    second_overhead_fixed=fields.Boolean(related='second_proposal_id.overhead_fixed', readonly=False, store=True)
    third_overhead_fixed=fields.Boolean(related='third_proposal_id.overhead_fixed', readonly=False, store=True)

    first_overhead_margin_fixed=fields.Float(related='first_proposal_id.overhead_margin_fixed', readonly=False)
    second_overhead_margin_fixed=fields.Float(related='second_proposal_id.overhead_margin_fixed', readonly=False)
    third_overhead_margin_fixed=fields.Float(related='third_proposal_id.overhead_margin_fixed', readonly=False)

    first_overhead_margin_percentage=fields.Float(related='first_proposal_id.overhead_margin_percentage', readonly=False)
    second_overhead_margin_percentage=fields.Float(related='second_proposal_id.overhead_margin_percentage', readonly=False)
    third_overhead_margin_percentage=fields.Float(related='third_proposal_id.overhead_margin_percentage', readonly=False)
    
    first_profit_margin=fields.Float(related='first_proposal_id.profit_margin', readonly=False)
    second_profit_margin=fields.Float(related='second_proposal_id.profit_margin', readonly=False)
    third_profit_margin=fields.Float(related='third_proposal_id.profit_margin', readonly=False)

    first_total_direct_cost=fields.Float(related='first_proposal_id.total_direct_cost')
    second_total_direct_cost=fields.Float(related='second_proposal_id.total_direct_cost')
    third_total_direct_cost=fields.Float(related='third_proposal_id.total_direct_cost')

    first_total_pricing_line=fields.Float(related='first_proposal_id.total_pricing_line')
    second_total_pricing_line=fields.Float(related='second_proposal_id.total_pricing_line')
    third_total_pricing_line=fields.Float(related='third_proposal_id.total_pricing_line')
    
    first_final_project_cost=fields.Float(related='first_proposal_id.final_project_cost')
    second_final_project_cost=fields.Float(related='second_proposal_id.final_project_cost')
    third_final_project_cost=fields.Float(related='third_proposal_id.final_project_cost')
    
    first_submitted=fields.Boolean(related='first_proposal_id.submitted', store=True)
    second_submitted=fields.Boolean(related='second_proposal_id.submitted', store=True)
    third_submitted=fields.Boolean(related='third_proposal_id.submitted', store=True)

    # CONSTRAINTS:
    @api.constrains('project_manager_id')
    def _check_project_manager_id(self):
        for record in self:
            if record.project_manager_id and not record.project_manager_id.active:
                raise ValidationError('The project manager must be an active employee!')
    
    @api.constrains('stage_id')
    def _check_won_stage(self):
        for record in self:
            if record.stage_id.is_won and not record.selected_pricing:
                raise ValidationError('User must select a pricing option before marking opportunity as "Won".')
    
    @api.constrains('selected_pricing')
    def _check_selected_pricing(self):
        for record in self:
            if record.stage_id.is_won:
                raise ValidationError('User cannot change pricing option after marking opportunity as "Won".')
    
    # COMPUTES:
    @api.depends('crm_lead_proposal_ids.proposal_number')
    def _compute_proposal_ids(self):
        for record in self:
            record.first_proposal_id=record.crm_lead_proposal_ids.filtered(lambda p: p.proposal_number == 'first')[:1] or False
            record.second_proposal_id=record.crm_lead_proposal_ids.filtered(lambda p: p.proposal_number == 'second')[:1] or False
            record.third_proposal_id=record.crm_lead_proposal_ids.filtered(lambda p: p.proposal_number == 'third')[:1] or False
    
    @api.depends('approved_proposal_id.final_project_cost')
    def _compute_selected_final_price(self):
        for record in self:
            record.selected_final_price=record.approved_proposal_id.final_project_cost
    
    # ACTIONS:
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
    
    def action_create_proposal(self):
        proposal_number=self.env.context.get('proposal_number')

        for record in self:
            record.env['crm.lead.proposal'].create([{'name': f'{record.name}\'s {proposal_number} proposal',
            'crm_lead_id': record.id,
            'proposal_number': proposal_number}])
    
    def action_submit(self):
        proposal_number=self.env.context.get('proposal_number')
        
        for record in self:
            if proposal_number=='first':
                record.first_proposal_id.action_submit()
            elif proposal_number=='second':
                record.second_proposal_id.action_submit()
            elif proposal_number=='third':
                record.third_proposal_id.action_submit()
    
    def action_withdraw(self):
        proposal_number=self.env.context.get('proposal_number')

        for record in self:
            if proposal_number=='first':
                record.first_proposal_id.action_withdraw()
            elif proposal_number=='second':
                record.second_proposal_id.action_withdraw()
            elif proposal_number=='third':
                record.third_proposal_id.action_withdraw()
    
    def action_approve_proposal(self):
        proposal_number=self.env.context.get('proposal_number')

        for record in self:
            if proposal_number=='first':
                record.approved_proposal_id=record.first_proposal_id
            elif proposal_number=='second':
                record.approved_proposal_id=record.second_proposal_id
            elif proposal_number=='third':
                record.approved_proposal_id=record.third_proposal_id
            record.expected_revenue=record.approved_proposal_id.final_project_cost
    
    def action_revoke_proposal(self):
        for record in self:
            record.approved_proposal_id=False
    
    def action_project_create(self):
        self.ensure_one()
        if not self.project_id and self.project_manager_id:
            self.project_id=self.env['project.project'].create([{'name': f'{self.name}\'s project'}])
            return self.action_project_view()
        elif self.project_id:
            raise ValidationError('Lead already has a project attached to it, a lead can only have one project.')
        else:
            raise ValidationError('A project_manager_id must be assigned before the project is created.')
    
    def action_project_view(self):
        self.ensure_one()
        action= self.env.ref('hst_pricing_tool.project_view_form').read()[0]
        action["res_id"]= self.project_id.id
        return action
    
    # def action_set_won_rainbowman(self):
    #     for record in self:
    #         if record.selected_pricing:
    #             super().action_set_won_rainbowman()
    #         else:
    #             raise ValidationError('User must select a pricing option before marking opportunity as "Won".')
    
    # ONCHANGES:
    @api.onchange('project_id')
    def _onchange_project_id(self):
        if self.project_id:
            self.project_id.user_id=self.project_manager_id