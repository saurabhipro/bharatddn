# -*- coding: utf-8 -*-


from odoo import http
from odoo.http import request
import uuid

def generate_slider_tab_token():
    token = str(uuid.uuid4())[:6]
#     token = int(ran_num[:5] + ran_num[-5:])  
#     token = uuid.uuid4().hex[:8]
    return str(token)


class portfolio(http.Controller):

    @http.route('/sh_onemate_theme/get_portfolio', auth='public', type='json',website=True)
    def portfolio(self,item_template = False):
        """
            Render Portfolio
            
        """
        portfolio_obj = request.env['website.portfolio']
        portfolio_category_obj = request.env['website.portfolio.category']        
        data = ''
        if item_template:
            

            categories = portfolio_category_obj.search([
                ('is_active','=',True),
                ('website_id', 'in', [request.website.id,False])
            ])
            
            Portfolios = portfolio_obj.search([
                ('is_active','=',True),
                ('website_id', 'in', [request.website.id,False]),
                ('category_id', 'in', categories.ids),
            ])
       
            token = generate_slider_tab_token()   

            data = request.env["ir.ui.view"]._render_template(item_template, values={
                'Portfolios': Portfolios,
                'categories': categories,
                'token': token,
            })


#         data = data.decode("utf-8")
        return data
    
