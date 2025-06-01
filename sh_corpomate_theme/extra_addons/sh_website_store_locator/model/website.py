# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields

class Website(models.Model):
    _inherit = 'website'

    sh_map_zoom = fields.Integer(
        string='Google Map Zoom',
        default=4
    )
    
    sh_store_locator_design_type = fields.Selection(
        string='Store Locator Design',
        selection=[
        ('style_1', 'Style 1'),
        ('style_2', 'Style 2')],
        default='style_1'
    )
    
    