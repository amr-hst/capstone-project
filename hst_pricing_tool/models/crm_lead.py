from odoo import api, fields, models
from odoo.exceptions import ValidationError

class HSTLead(models.Model):
    _inherit="crm.lead"
    _sql_constraints=[
        ("unique_project_id", "unique(project_id)", "Each CRM lead can only have one project, and vice versa."),
    ]
    
    #CRM Project Pricing Tools fields:
    project_id=fields.Many2one("project.project")
    project_manager_id=fields.Many2one("hr.employee")
    selected_pricing=fields.Selection([("standard", "Standard Margins"),
                                ("competitive", "Competitive Margins"),
                                ("high", "High Margins")])
    selected_final_price=fields.Float()
    crm_lead_proposal_ids=fields.One2many("crm.lead.proposal", "crm_lead_id")


    @api.constrains('project_manager_id')
    def _check_project_manager_id(self):
        for record in self:
            if not record.project_manager_id.active:
                raise ValidationError("The project manager must be an active employee!")