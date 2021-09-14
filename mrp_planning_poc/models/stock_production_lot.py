from odoo import _, api, fields, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    volume = fields.Float(string="Volume")

    project_id = fields.Many2one(string="Project", comodel_name="project.project")
