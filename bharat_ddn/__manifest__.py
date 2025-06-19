# -*- coding: utf-8 -*-
{
    'name': 'Bharat DDN',
    'summary': """
        Property Survey Management System for Suryabinayak Municipality
    """,
    'description': """
        Property Survey Management System for Suryabinayak Municipality
    """,
    'author': 'Windsurf',
    'website': 'https://www.windsurf.io',
    'category': 'Services/Property',
    'version': '0.1',
    'depends': ['base', 'mail', 'web', 'report_xlsx'],
    'data': [
        # Security
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        
        
        # Views
        'views/zone_views.xml',
        'views/ward_views.xml',
        'views/colony_views.xml',
        'views/property_type_views.xml',
        'views/property_views.xml',
        'views/property_map_view.xml',
        'views/res_users_views.xml',
        'views/mobile_otp_views.xml',
        'views/jwt_token_views.xml',
        'views/property_survey_views.xml',
        'views/property_group_views.xml',
        'views/services_views.xml',
        'views/dashboard.xml',
        'views/res_company_views.xml',
        'wizard/property_import_wizard_view.xml',
        'wizard/ddn_report.xml',

        'views/property_id_data_views.xml',
        'views/menuitems.xml',  # Load menus last
        # 'views/assets.xml',
    ],
    'assets': {
        'web.assets_backend': [
            # Components
            # 'bharat_ddn/static/src/components/kpi_card/kpi_card.js',
            # 'bharat_ddn/static/src/components/kpi_card/kpi_card.xml',
            'bharat_ddn/static/src/components/google_map/property_map.js',
            'bharat_ddn/static/src/components/google_map/property_map_template.xml',
            'bharat_ddn/static/src/components/dashboard/dashboard.js',
            'bharat_ddn/static/src/components/dashboard/dashboard.xml',
            'bharat_ddn/static/src/components/dashboard/dashboard.scss',
            'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css',
            'https://maps.googleapis.com/maps/api/js?key=AIzaSyCQ1XvoKRmX1qqo2XwlLj2C2gCIiCjtgFE&callback=Function.prototype',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
