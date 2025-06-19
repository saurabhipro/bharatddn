{
    "name": "Strategy MA",
    "version": "1.0",
    "category": "Contacts",
    "summary": "Adds custom fields to Contacts",
    "author": "IPROSONIC",
    "depends": ["base"],
    "data": [
        'security/ir.model.access.csv',
        'views/company_type_views.xml',
        'views/res_partner_views.xml',
    ],
    "installable": True,
    "application": False,
    "auto_install": False
}
