# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api


class ShNbNoticeBoard(models.Model):
    _name = 'sh.nb.notice.board'
    _inherit = ['website.published.multi.mixin']
    _description = 'Notice board for display news on website'
    _order = 'sequence ASC'

    # Get Default Website
    def default_website(self):
        company_id = self.env.company.id

        if self._context.get('default_company_id'):
            company_id = self._context.get('default_company_id')

        domain = [('company_id', '=', company_id)]
        return self.env['website'].search(domain, limit=1)

    name = fields.Char('Title', required=True, translate=True)
    sequence = fields.Integer('Sequence')
    desc = fields.Text('Description', translate=True)
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company
    )
    nb_image = fields.Image("Image")
    
    @api.model_create_multi
    def create(self, vals):
        res = super(ShNbNoticeBoard, self).create(vals)
        for news in res:
            news.sequence = news.id            
        return res

    def action_active_inactive(self):
        if self.active == False:
            self.active = True
        else:
            self.active = False      
