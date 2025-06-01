# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models
import json

class ShWebsiteStoreLocator(models.Model):
    _name = 'sh.website.store.locator'
    _description = 'Website Store Locator'

    name = fields.Char('Store Name', translate=True)
    sh_store_img = fields.Image("Image")

    # address
    sh_street = fields.Char()
    sh_street2 = fields.Char()
    sh_zip = fields.Char(change_default=True)
    sh_city = fields.Char()
    sh_state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict')
    sh_country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')

    # contact details
    sh_contact_name = fields.Char('Name')
    sh_contact_mobile = fields.Char('Mobile')
    sh_contact_phone = fields.Char('Phone')
    sh_contact_email = fields.Char('Email')
    sh_contact_fax = fields.Char('Fax')
    sh_contact_website = fields.Char('Website')

    # days
    sh_days_from = fields.Selection(
        string='Day From',
        selection=[
        ('mon', 'Monday'),
        ('tue', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thu', 'Thursday'),
        ('fri', 'Friday'),
        ('sat', 'Saturday'),
        ('sun', 'Sunday'),
        ]
    )
    sh_days_to = fields.Selection(
        string='Day To',
        selection=[
        ('mon', 'Monday'),
        ('tue', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thu', 'Thursday'),
        ('fri', 'Friday'),
        ('sat', 'Saturday'),
        ('sun', 'Sunday'),
        ]
    )
    sh_time_from = fields.Float(
        string='Time From',
        default=0.00
    )
    sh_time_to = fields.Float(
        string='Time To',
        default=0.00
    )

    # Tags
    sh_store_tag_ids = fields.Many2many(
        string='Tags',
        comodel_name='sh.website.store.tags',
    )

    active = fields.Boolean(
        string='Active',
        default=True,
    )

    # long and lat
    sh_latitude = fields.Float('Latitude N',digits=(16, 5))
    sh_longitude = fields.Float('Longitude E',digits=(16, 5))

    # Auto complete
    sh_contact_google_location = fields.Char('Enter Location')
    sh_contact_place_text = fields.Char('Enter location', copy=False)
    sh_contact_place_text_main_string = fields.Char(
        'Enter location ', copy=False)
    

    @api.onchange('sh_contact_place_text_main_string')
    def onchange_technical_google_text_main_string(self):
        """to seve name in google field"""

        if self.sh_contact_place_text_main_string:
            self.sh_contact_google_location = self.sh_contact_place_text_main_string

    @api.onchange('sh_contact_place_text')
    def onchange_technical_google_text(self):
        """to place info to std. address fields"""

        if self.sh_contact_place_text:
            google_place_dict = json.loads(self.sh_contact_place_text)

            if google_place_dict and google_place_dict.get('postcode', ''):
                self.sh_zip = google_place_dict.get('postcode', '')
            else:
                self.sh_zip = ''

            if google_place_dict and google_place_dict.get('street', ''):
                self.sh_street = google_place_dict.get('street', '')
            else:
                self.sh_street = ''

            if google_place_dict and google_place_dict.get('street2', ''):
                self.sh_street2 = google_place_dict.get('street2', '')
            else:
                self.sh_street2 = ''

            if google_place_dict and google_place_dict.get('city', ''):
                self.sh_city = google_place_dict.get('city', '')
            else:
                self.sh_city = ''

            if google_place_dict and google_place_dict.get('country', False):
                self.sh_country_id = google_place_dict.get('country', False)
            else:
                self.sh_country_id = False

            if google_place_dict and google_place_dict.get('state', False):
                self.sh_state_id = google_place_dict.get('state', False)
            else:
                self.sh_state_id = False
            
            if google_place_dict and google_place_dict.get('latitude', False):
                self.sh_latitude = google_place_dict.get('latitude', False)
            else:
                self.sh_latitude = False
            
            if google_place_dict and google_place_dict.get('longitude', False):
                self.sh_longitude = google_place_dict.get('longitude', False)
            else:
                self.sh_longitude = False
    
    
    