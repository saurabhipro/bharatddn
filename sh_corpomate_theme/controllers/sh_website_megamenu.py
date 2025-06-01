# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo.http import request
from odoo import http


class ShWebsiteMegaMenu(http.Controller):

    # --------------------------------------------------------------------------
    # Design Mega Menu Editor
    # --------------------------------------------------------------------------
    @http.route('/sh_website_megamenu/design_mega_menu', type='http', auth="user", website=True)
    def design_mega_menu(self, menu_id=False, **kw):
        if menu_id and not isinstance(menu_id, int):
            menu_id = int(menu_id)
        record = False
        if menu_id:
            record = request.env["website.menu"].browse(menu_id)

        values = {'record': record}
        return request.render("sh_corpomate_theme.sh_website_megamenu_design_mega_menu_tmpl", values)

    # --------------------------------------------------------------------------
    # Prepare Products Vals
    # --------------------------------------------------------------------------

    # def _prepare_categories_vals(self, categories):
    #     fields = ['id', 'name']
    #     res = {}
    #     res.update({'categories': categories.read(fields)})
    #     return res.get('categories')

    def _prepare_categories_vals(self, categories):
        # fields = ['id', 'name']
        # res = {}
        list_categories_dic = []
        for categ in categories:
            list_categories_dic.append({
                'id':categ.id,
                'name': categ.name,
                'categ_obj': categ
            })
        return list_categories_dic
        # res.update({'categories': categories.read(fields)})
        # return res.get('categories')
        # res.update({'categories': categories.read(fields)})
        # value =  res.get('categories')
        # return value
    # --------------------------------------------------------------------------
    # Get Dynamic Mega Menu Content
    # --------------------------------------------------------------------------
    @http.route('/sh_website_megamenu/get_content', type='json', auth='public', website=True)
    def get_content(self, item_template=False, filter_id=False, **kwargs):
        res = {}
        data = ''
        sh_mega_menu_config = False
        list_categs_dic = []

        # --------------------------------------------------------------------------
        # Find Filters
        if filter_id:
            sh_mega_menu_config = request.env['sh.mega.menu.config'].sudo().search(
                [('id', '=', filter_id)], limit=1)

        if sh_mega_menu_config and sh_mega_menu_config.categ_line:
            for line in sh_mega_menu_config.categ_line:
                if line.category_id:
                    parent_categ_dic = self._prepare_categories_vals(line.category_id)[
                        0]
                    parent_categ_dic['list_sub_categs_dic'] = []

                    if line.sub_category_ids:
                        parent_categ_dic.update(
                            {'list_sub_categs_dic': self._prepare_categories_vals(line.sub_category_ids)})
                    list_categs_dic.append(parent_categ_dic)
        res.update({'list_categs_dic': list_categs_dic })
        data = request.env["ir.ui.view"].sudo(
        )._render_template(item_template, values=res)
        #data = data.decode("utf-8")
        values = {'data': data}
        return values
