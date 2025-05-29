from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    plate_background_image = fields.Binary(string='Plate Background Image', attachment=True, help='Upload the background image for property plates.') 