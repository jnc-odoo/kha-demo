{
    "name": "Mrp Planning Poc",
    "summary": """
        Mrp Planning Poc scaffold module
        """,
    "category": "",
    "version": "14.0.1.0.4",
    "author": "Odoo PS",
    "website": "http://www.odoo.com",
    "license": "OEEL-1",
    "depends": [
        'mrp',
        'stock',
        'project',
        'planning',
    ],
    "data": [
        "security/ir.model.access.csv",

        "views/capacity_planning.xml",
        "views/mrp_production.xml",
        "views/mrp_workcenter.xml",
        "views/stock_production_lot.xml",

    ],
    # Only used to link to the analysis / Ps-tech store
    "task_id": [0],
}
