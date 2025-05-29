from odoo import models, fields, api, _

class Colony(models.Model):
    _name = 'ddn.colony'
    _description = 'Colony'

    name = fields.Char(string='Name')
    ward_id = fields.Many2one('ddn.ward', string='Ward')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self : self.env.company.id, readonly=True)
    active = fields.Boolean(string='Active', default=True)
    code = fields.Char(string='Code')
