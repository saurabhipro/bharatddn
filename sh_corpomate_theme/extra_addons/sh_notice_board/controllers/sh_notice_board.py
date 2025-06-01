# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import http
from odoo.osv import expression
from odoo.http import request


class Main(http.Controller):

    @http.route('/get_latest_news', type='json', auth='public', website=True)
    def get_latest_news(self, limit=False):
        limit = int(limit)
        domain = [('active', '=', True), ('is_published', '=', True)]
        domain = expression.AND([domain, ['|', ('website_id', '=', request.website.id), ('website_id', '=', False)]])
        
        latest_news_records = request.env['sh.nb.notice.board'].sudo().search_read(domain, limit=limit, order="sequence asc",)
        return latest_news_records
