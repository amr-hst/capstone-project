from odoo import fields, models

class HSTLinkedProject(models.Model):
    _inherit="project.project"

    crm_ids=fields.One2many("crm.lead", "project_id")
    