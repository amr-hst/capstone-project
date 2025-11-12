{
    "name": "HST Pricing Tool",
    "version": "18.0.1.0,0",
    "category": "Hidden",
    "summary": """Odoo 18 CRM, Odoo 18 Project, Odoo 18 CRM Leads, Odoo18 CRM, Odoo18 Project, Odoo crm, Odoo project, Odoo18, CRM, Project, Odoo Apps""",
    "description": """Odoo 18 CRM & Project, a comprehensive CRM Project Pricing Tools module that integrates project management capabilities with advanced pricing calculations within Odoo 18.
    
    The CRM Project Pricing Tools module extends Odoo's CRM functionality to provide:
    •	Project Integration: Direct project creation from CRM opportunities
    •	Three-Tier Pricing System: Multiple pricing scenarios for different market conditions
    •	Cost Management: Employee costs, direct costs, overhead calculations
    •	Profit Analysis: Automated profit margin calculations and final pricing
    """,
    "author": "Amr Mahadeen",
    "company": "Hamilton Smart Technologies",
    "maintainer": "Amr Mahadeen",
    "depends": ["base", "project", "crm", "hr", "timesheet_grid"],
    "data": [
        "views/crm_lead_views.xml",
        "views/crm_lead_proposal_views.xml",
        "views/crm_menu_views.xml",
        "views/project_project_views.xml",
        "security/ir.model.access.csv",
    ],
    "license":"LGPL-3",
}