from odoo import _, api, fields, models


class MrpWorkcenter(models.Model):
    _inherit = "mrp.workcenter"

    weekly_capacity = fields.Float(string="Weekly capacity")
