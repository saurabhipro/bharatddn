from odoo import models, fields

class CompanyType(models.Model):
    _name = 'company.type'
    _description = 'Company Type'

    name = fields.Char(string='Company Type', required=True, translate=True)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    x_last_name = fields.Char(string="Last Name.")
    x_contact_source = fields.Char(string="Contact Source", search=True)
    x_linkedin_url = fields.Char(string="LinkedIn URL", search=True)
    x_company_type = fields.Many2one('company.type', string='Company Type')
    x_company_industry = fields.Many2one('res.partner.industry', string='Company Industry')
