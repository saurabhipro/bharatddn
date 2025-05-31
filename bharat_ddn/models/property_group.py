from odoo import models, fields, api
import uuid

class PropertyGroup(models.Model):
    _name = 'ddn.property.group'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Property Group'

    name = fields.Char(string='Group Name', required=True, tracking=True)
    active = fields.Boolean(string='Active', default=True, tracking=True)
    uuid = fields.Char(string='UUID', readonly=True, copy=False, default=lambda self: str(uuid.uuid4()))
    company_id = fields.Many2one('res.company', string="Company", default=lambda self : self.env.company.id, readonly=True)


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('uuid'):
                vals['uuid'] = str(uuid.uuid4())
        return super(PropertyGroup, self).create(vals_list) 