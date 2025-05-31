from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    plate_background_image = fields.Binary(string='Plate Background Image', attachment=True, help='Upload the background image for property plates.') 
    s3_bucket_base_url = fields.Char(string='S3 Bucket Base URL', help='Base URL for the S3 bucket (e.g., https://your-bucket.s3.amazonaws.com/)') 