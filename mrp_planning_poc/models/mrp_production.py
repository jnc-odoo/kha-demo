from odoo import _, api, fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    volume = fields.Float(string="Volume")

    project_id = fields.Many2one(string="Project", comodel_name="project.project")

    capacity_planning_id = fields.Many2one(comodel_name='capacity.planning')
