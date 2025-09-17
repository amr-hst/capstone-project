from odoo import fields, models

class DirectCost(models.Model):
    _name="direct.cost"
    
    crm_lead_proposal_id=fields.Many2one("crm.lead.proposal")
    other_cost=fields.Char()
    cost_amount=fields.Float()
    # pricing_type=fields.

#     other_cost: Cost description
# cost_amount: Cost value
# pricing_type: Associated pricing tier