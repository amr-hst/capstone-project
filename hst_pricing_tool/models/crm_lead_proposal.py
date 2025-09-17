from odoo import fields, models

class CRMProposals(models.Model):
    _name="crm.lead.proposal"
    _sql_constraints=[
        ("unique_lead_proposal", "unique(crm_lead_id, proposal_number)", "Ensures there are no duplicates amongst the pairs of the 'crm_lead_id' & 'proposal_number' fields, meaning there can only be three proposals per lead.")
    ]

    crm_lead_id=fields.Many2one("crm.lead")
    proposal_number=fields.Selection([("first", "First"),
                                ("second", "Second"),
                                ("third", "Third")])
    direct_cost_ids=fields.One2many("direct.cost", "crm_lead_proposal_id")
    pricing_line_ids=fields.One2many("pricing.line", "crm_lead_proposal_id")
    overhead_margin=fields.Float()
    profit_margin=fields.Float()
    total_direct_cost=fields.Float()
    total_pricing_line=fields.Float()