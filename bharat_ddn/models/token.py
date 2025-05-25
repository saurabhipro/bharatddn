from odoo import models, fields

class JWTToken(models.Model):
    _name = 'jwt.token'
    _description = 'JWT Token'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    user_id = fields.Many2one('res.users', string='User', required=True)
    token = fields.Char(string='Token', required=True)
    company_id = fields.Many2one('res.company', string="Company", default=lambda self : self.env.company.id, readonly=True)


