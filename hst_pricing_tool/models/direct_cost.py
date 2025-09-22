from odoo import fields, models

class DirectCost(models.Model):
    _name="direct.cost"
    
    crm_lead_proposal_id=fields.Many2one("crm.lead.proposal", ondelete='cascade')
    name=fields.Char(required=True)
    amount=fields.Float(required=True)