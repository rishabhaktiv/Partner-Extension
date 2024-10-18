# -*- coding: utf-8 -*-

{
    "name": "Contact Customization",
    "version": "17.0.0.0.1",
    "category": "Sale/Invoice",
    "summary": "Contact Customization",
    "description": """
        Contact Customization
        """,
    "author": "Aktiv Software",
    "company": "Aktiv Software",
    "website": "https://www.aktivsoftware.com",
    "depends": ["sale_management", "account", "auth_signup"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_extended_views.xml",
        "views/res_partner_extended_menus.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
    "license": "LGPL-3",
}
