from odoo import models, fields, api
import uuid

class PropertyType(models.Model):
    _name = 'ddn.property.type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Property Type'

    name = fields.Char(string='Type', required=True, tracking=True)
    active = fields.Boolean(string='Active', default=True, tracking=True)
    company_id = fields.Many2one('res.company', string="Company", default=lambda self : self.env.company.id, readonly=True)
    group_id = fields.Many2one('ddn.property.group', string='Property Group', tracking=True)
    uuid = fields.Char(string='UUID', readonly=True, copy=False, default=lambda self: str(uuid.uuid4()))

    # @api.model_create_multi
    # def create(self, vals_list):
    #     for vals in vals_list:
    #         if not vals.get('uuid'):
    #             vals['uuid'] = str(uuid.uuid4())
    #     return super(PropertyType, self).create(vals_list)
