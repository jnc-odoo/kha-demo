from odoo import _, api, fields, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    volume = fields.Float(string="Volume")

    project_id = fields.Many2one(string="Project", comodel_name="project.project")

    production_ids = fields.One2many('mrp.production', 'lot_producing_id')

    capacity_planning_ids = fields.Many2many(string="Element", comodel_name="capacity.planning")
