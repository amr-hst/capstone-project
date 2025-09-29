from odoo import api, fields, models
from odoo.exceptions import ValidationError

class DirectCost(models.Model):
    _name="direct.cost"
    
    crm_lead_proposal_id=fields.Many2one("crm.lead.proposal", ondelete='cascade')
    name=fields.Char(required=True)
    amount=fields.Float(required=True)

    @api.constrains('amount')
    def _check_amount(self):
        for record in self:
            if record.amount < 0:
                raise ValidationError('A direct cost\'s amount cannot be negative')