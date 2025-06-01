# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields


class WebsitePortfolioCategory(models.Model):
    _name = "website.portfolio.category"
    _description = "Website Portfolio Category"

    name = fields.Char(string="Category", required=True, translate=True)
    is_active = fields.Boolean(string="Active", default=True)
    website_id = fields.Many2one('website', required=True)

class WebsitePortfolio(models.Model):
    _name = "website.portfolio"
    _description = "Website Portfolio"

    category_id = fields.Many2one("website.portfolio.category",
                                  string="Category",
                                  required=True)
    img = fields.Image(string="Image", help="preffered size 300x300")
    name = fields.Char(string="Title", required=True, translate=True)
    desc = fields.Text(string="Description", translate=True)
    is_active = fields.Boolean(string="Active", default=True)
    company_id = fields.Many2one("res.company",
                                 string="Company",
                                 default=lambda self: self.env.company)
    website_id = fields.Many2one("website",
                                 related="category_id.website_id",
                                 required=True,
                                 readonly=True)
    url = fields.Char('URL')
    button_color = fields.Char('Button Color',default='#92c516')
    button_text = fields.Char('Button Text',translate=True)
