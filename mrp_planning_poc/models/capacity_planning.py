from odoo import _, api, fields, models


class CapacityPlanning(models.Model):
    _name = "capacity.planning"
    _description = "Capacity planning"

    name = fields.Char()
    production_nesting = fields.Char(string="Production nesting")
    production_week = fields.Date(string="Production week")
    delivery_week = fields.Date(string="Delivery week")
    actual_volume = fields.Float(string="Actual volume", compute="_actual_volume")
    complexity_ratio = fields.Float(string="Complexity", default=1.0)
    planning_volume = fields.Float(string="Planning volume", compute="_planning_volume")
    capacity = fields.Float(string="Capacity", compute="_compute_capacity")
    element_ids = fields.Many2many(string="Element", comodel_name="stock.production.lot", compute="_compute_element_ids")
    mill_id = fields.Many2one(string="Mill", comodel_name="mrp.workcenter")
    mill_capacity = fields.Float(related='mill_id.weekly_capacity')
    responsible_id = fields.Many2one(string="Responsible", comodel_name="res.users")
    type = fields.Selection(string="Type", selection=[("contract", "Contract"), ("reservation", "Reservation")])
    notes = fields.Text(string="Notes")
    project_id = fields.Many2one(string="Project", comodel_name="project.project")

    @api.depends('project_id')
    def _compute_element_ids(self):
        for planning in self:
            planning.element_ids = self.env['stock.production.lot'].search([('project_id', '=', planning.project_id.id)])

    @api.depends('element_ids')
    def _actual_volume(self):
        for planning in self: 
            planning.actual_volume = sum(planning.element_ids.mapped('volume'))

    @api.depends('actual_volume', 'complexity_ratio')
    def _planning_volume(self):
        for planning in self: 
            planning.planning_volume = planning.complexity_ratio * planning.actual_volume

    @api.depends('planning_volume', 'mill_capacity')
    def _compute_capacity(self):
        for planning in self:
            # POOOOC, inneficient
            total_planning_volume_per_week = sum(self.env['capacity.planning']\
                .search([('mill_id', '=', planning.mill_id.id)])\
                .filtered(lambda p: p.production_week and planning.production_week and p.production_week.isocalendar()[1] == planning.production_week.isocalendar()[1])\
                .mapped('planning_volume'))
            planning.capacity = total_planning_volume_per_week / planning.mill_capacity * 100 if planning.mill_capacity else 0

    def action_create_mo(self):
        for planning in self:
            for lot in planning.element_ids:
                self.env['mrp.production'].create({
                    'lot_producing_id': lot.id,
                    'product_id': lot.product_id.id,
                    'product_uom_id': lot.product_uom_id.id,
                    'volume': False,
                    'project_id': planning.project_id.id,
                    'date_planned_start': planning.production_week,
                    'origin': 'Planning %s' % planning.name,
                })