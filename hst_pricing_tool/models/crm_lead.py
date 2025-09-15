from odoo import fields, models

class HSTLead(models.Model):
    _inherit="crm.lead"
    _sql_constraints=[
        ("unique_project_id", "unique(project_id)", "Each CRM lead can only have one project, and vice versa.")
    ]
    
    #CRM Project Pricing Tools fields:
    project_id=fields.Many2one("project")
    project_manager_id=fields.Many2one("hr.employee")
    selected_pricing=fields.Selection([("")])
    selected_final_price=fields.Float()