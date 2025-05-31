from odoo import models, fields, api

class Ward(models.Model):
    _name = 'ddn.ward'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Ward'

    name = fields.Char(string='Ward Name', required=True, tracking=True)
    code = fields.Char(string='Ward Code', tracking=True)
    zone_id = fields.Many2one('ddn.zone', string='Zone', tracking=True)
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True, tracking=True)
    pdf_url = fields.Char(string='PDF URL', tracking=True)
    property_count = fields.Integer(string="Property Count", compute="_action_property_count", readonly=True, store=True)
    company_id = fields.Many2one('res.company', string="Company", default=lambda self : self.env.company.id, readonly=True)

    _sql_constraints = [
        ('unique_ward_name_per_zone', 'unique(name, zone_id)', 'Ward name must be unique within a zone!'),
    ]

    
    def _action_property_count(self):
        property_count = self.env['ddn.property.info'].search_count([('company_id','=',self.company_id.id),('ward_id','=',self.id)])
        self.property_count = property_count
            

    def update_ward(self):
        """ This function will update the pdf_url field and return a dynamic URL. """
        config_parameter = self.env['ir.config_parameter'].sudo()
        base_url = config_parameter.get_param('web.base.url', default=False)

        new_pdf_url = f"{base_url}/download/ward_properties_pdf?ward_id={(self.id)}" 
        self.write({'pdf_url': new_pdf_url})
        property = self.env['ddn.property.info'].search([('ward_id','=',self.id)])
        property.write({'property_status' : 'pdf_downloaded'})

        return {
                'type': 'ir.actions.act_url',
                'url': '/download/ward_properties_pdf?ward_id=%s' % (self.id),
                'target': 'new',
            } 