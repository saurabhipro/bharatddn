# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo.http import request
from odoo import http, fields, _
from odoo.exceptions import UserError
from odoo import http
from datetime import datetime
from odoo.tools.safe_eval import safe_eval

from odoo.addons.website.controllers.main import Website


from markupsafe import Markup


class Website_odoo16(Website):

    @http.route()
    def theme_customize_data(self, is_view_data, enable=None, disable=None, reset_view_arch=False):
        TOTAL_THEME = 6
        TOTAL_THEME = TOTAL_THEME + 1
        # --------------------------------------
        # Footer Individual Change
        # --------------------------------------
        if len(enable) == 1 and any("sh_corpomate_theme.sh_corpomate_theme_footer_custom_" in s for s in enable):
            # whatever
            matching = [
                s for s in enable if "sh_corpomate_theme.sh_corpomate_theme_footer_custom_" in s]
            if matching and len(matching) == 1:
                matching_string = matching[0] or ''
                matching_theme_number = matching_string.replace(
                    'sh_corpomate_theme.sh_corpomate_theme_footer_custom_', '')
                if matching_theme_number:
                    i = 1
                    while i < TOTAL_THEME:
                        # Footer SCSS
                        asset = request.env.ref('sh_corpomate_theme.sh_corpomate_theme_style_footer_scss_%s' % (
                            i), raise_if_not_found=False)
                        if asset:
                            asset.write({'active': False})

                        i += 1
                    # Footer SCSS
                    to_active_asset = 'sh_corpomate_theme.sh_corpomate_theme_style_footer_scss_' + \
                        matching_theme_number
                    asset = request.env.ref(
                        to_active_asset, raise_if_not_found=False)
                    if asset:
                        asset.write({'active': True})

        if any("sh_corpomate_theme.sh_corpomate_theme_layout_readymade_" in s for s in enable):
            matching = [
                s for s in enable if "sh_corpomate_theme.sh_corpomate_theme_layout_readymade_" in s]
            if matching and len(matching) == 1:
                matching_string = matching[0] or ''
                matching_theme_number = matching_string.replace(
                    'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_', '')
                if matching_theme_number:
                    i = 1
                    while i < TOTAL_THEME:
                        # Header SCSS
                        asset = request.env.ref('sh_corpomate_theme.sh_corpomate_theme_style_header_scss_%s' % (
                            i), raise_if_not_found=False)
                        if asset:
                            asset.write({'active': False})
                        # Footer SCSS
                        asset = request.env.ref('sh_corpomate_theme.sh_corpomate_theme_style_footer_scss_%s' % (
                            i), raise_if_not_found=False)
                        if asset:
                            asset.write({'active': False})
                        # Color SCSS
                        asset = request.env.ref('sh_corpomate_theme.sh_corpomate_theme_primary_variable_color_scss_%s' % (
                            i), raise_if_not_found=False)
                        if asset:
                            #asset.write({'active': False})
                            query = """
                                UPDATE ir_asset
                                    SET active = false
                                WHERE id = %s;
                            """ % (asset.id)
                            request.env.cr.execute(query)
                        # Font SCSS
                        asset = request.env.ref('sh_corpomate_theme.sh_corpomate_theme_primary_variable_font_scss_%s' % (
                            i), raise_if_not_found=False)
                        if asset:
                            #asset.write({'active': False})
                            query = """
                                UPDATE ir_asset
                                    SET active = false
                                WHERE id = %s;
                            """ % (asset.id)
                            request.env.cr.execute(query)
                        i += 1

                    # Header SCSS
                    to_active_asset = 'sh_corpomate_theme.sh_corpomate_theme_style_header_scss_' + \
                        matching_theme_number
                    asset = request.env.ref(
                        to_active_asset, raise_if_not_found=False)
                    if asset:
                        asset.write({'active': True})
                    # Footer SCSS
                    to_active_asset = 'sh_corpomate_theme.sh_corpomate_theme_style_footer_scss_' + \
                        matching_theme_number
                    asset = request.env.ref(
                        to_active_asset, raise_if_not_found=False)
                    if asset:
                        asset.write({'active': True})
                    # Color SCSS
                    to_active_asset = 'sh_corpomate_theme.sh_corpomate_theme_primary_variable_color_scss_' + \
                        matching_theme_number
                    asset = request.env.ref(
                        to_active_asset, raise_if_not_found=False)
                    if asset:
                        # asset.write({'active': True})
                        query = """
                            UPDATE ir_asset
                                SET active = true
                            WHERE id = %s;
                        """ % (asset.id)
                        request.env.cr.execute(query)
                    # Font SCSS
                    to_active_asset = 'sh_corpomate_theme.sh_corpomate_theme_primary_variable_font_scss_' + \
                        matching_theme_number
                    asset = request.env.ref(
                        to_active_asset, raise_if_not_found=False)
                    if asset:
                        # asset.write({'active': True})
                        query = """
                            UPDATE ir_asset
                                SET active = true
                            WHERE id = %s;
                        """ % (asset.id)
                        request.env.cr.execute(query)
        # ==============================================================
        # FOR READYMADE THEME
        # ==============================================================
        list_readymade_tmpl = [
            'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_1',
            'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_2',
            'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_3',
            'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_4',
            'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_5',
            'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_6',
            'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_none',
        ]

        # ======================================================
        # STEP 1: CHECK IF CHANGED IN READYMADE THEME
        # ======================================================
        selected_readymade_tmpl = ''
        is_readymade_theme_changed = False
        list_to_delete_menu_ids = []
        list_keep_menu_data_dic = []
        list_to_delete_home_page_menu_ids = []
        for item in list_readymade_tmpl:
            if item in enable:
                selected_readymade_tmpl = item
                is_readymade_theme_changed = True
                break

#         multiwebsite_domain = [
#             ("website_id",'=', request.website.id),
#         ]

        multiwebsite_domain = request.website.website_domain()

        if is_readymade_theme_changed:

            # ======================================================
            # MANAGE LIST OF OUR PAGES VIEW KEY
            # ======================================================

            list_page_theme_1 = [
                'sh_corpomate_theme.sh_corpomate_tmpl_about_us_1',
                'sh_corpomate_theme.sh_corpomate_tmpl_contact_us_1',
                'sh_corpomate_theme.sh_corpomate_tmpl_home_1',
                'sh_corpomate_theme.sh_corpomate_tmpl_service_1',
                'sh_corpomate_theme.sh_corpomate_tmpl_our_team_1',
            ]
            list_page_theme_2 = [
                'sh_corpomate_theme.sh_corpomate_tmpl_about_us_2',
                'sh_corpomate_theme.sh_corpomate_tmpl_contact_us_2',
                'sh_corpomate_theme.sh_corpomate_tmpl_home_2',
                'sh_corpomate_theme.sh_corpomate_tmpl_service_2',
            ]
            list_page_theme_3 = [
                'sh_corpomate_theme.sh_corpomate_tmpl_about_us_3',
                'sh_corpomate_theme.sh_corpomate_tmpl_contact_us_3',
                'sh_corpomate_theme.sh_corpomate_tmpl_home_3',
                'sh_corpomate_theme.sh_corpomate_tmpl_service_3',
                'sh_corpomate_theme.sh_corpomate_tmpl_project_3',
                'sh_corpomate_theme.sh_corpomate_tmpl_gallery_3',
            ]

            list_page_theme_4 = [
                'sh_corpomate_theme.sh_corpomate_tmpl_about_us_4',
                'sh_corpomate_theme.sh_corpomate_tmpl_contact_us_4',
                'sh_corpomate_theme.sh_corpomate_tmpl_home_4',
                'sh_corpomate_theme.sh_corpomate_tmpl_service_4',
                'sh_corpomate_theme.sh_corpomate_tmpl_portfolio_4',
                'sh_corpomate_theme.sh_corpomate_tmpl_our_team_4',
            ]
            list_page_theme_5 = [
                'sh_corpomate_theme.sh_corpomate_tmpl_home_5',
                
            ]
            list_page_theme_6 = [
                'sh_corpomate_theme.sh_corpomate_tmpl_home_6',
                
            ]
            

            theme_none_list_page = list_page_theme_1 + list_page_theme_2 + list_page_theme_3  + list_page_theme_4 + list_page_theme_5+ list_page_theme_6

            dic_page_list = {
                'theme_1': list_page_theme_1,
                'theme_2': list_page_theme_2,
                'theme_3': list_page_theme_3,
                'theme_4': list_page_theme_4,
                'theme_5': list_page_theme_5,
                'theme_6': list_page_theme_6,
                'theme_none': theme_none_list_page
            }

            # FIND VIEW IDS FOR ALL THEME AND MAKE DICTIONARY
            dic_page_view_ids_list = {}
            for key, value in dic_page_list.items():
                list_view_ids = []
                view_pages = request.env['ir.ui.view'].sudo().search([
                    ('key', 'in', value)
                ])
                if view_pages.sudo():
                    list_view_ids = view_pages.sudo().ids

                dic_page_view_ids_list.update({
                    key: list_view_ids
                })

            if dic_page_view_ids_list:

                # ======================================================
                # STEP 2 HIDE OUR ALL PAGES
                # ======================================================
                ids = sum(dic_page_view_ids_list.values(), [])
                page_domain = [('view_id', 'in', ids)]

                # UNPUBLISH ALL OUR PAGES.
                pages = request.env['website.page'].sudo().search(
                    page_domain + multiwebsite_domain)

                if pages:
                    #                     pages.sudo().write({
                    #                         'website_published': False,
                    #                         })

                    # delete all menu here
                    menu_ids_list = []
                    for page in pages:
                        if page.menu_ids:
                            menu_ids_list += page.menu_ids.ids

                    menu_domain = [
                        ('id', 'in', menu_ids_list),
                        ("website_id", '=', request.website.id),
                    ]
                    menus = request.env['website.menu'].sudo().search(
                        menu_domain)

                    if menus:
                        list_to_delete_menu_ids = menus.ids
                        # pass
                        # commented in odoo16 migration
                        menus.sudo().unlink()

                # delete all menu here
                # ======================================================
                # STEP 2 HIDE OUR ALL PAGES
                # ======================================================

                # ======================================================
                # STEP 3 SHOW SELECTED THEME PAGES
                # ======================================================

                if selected_readymade_tmpl == 'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_1':
                    page_domain = [
                        ('view_id', 'in', dic_page_view_ids_list.get("theme_1", []))]

                elif selected_readymade_tmpl == 'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_2':
                    page_domain = [
                        ('view_id', 'in', dic_page_view_ids_list.get("theme_2", []))]

                elif selected_readymade_tmpl == 'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_3':
                    page_domain = [
                        ('view_id', 'in', dic_page_view_ids_list.get("theme_3", []))]

                elif selected_readymade_tmpl == 'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_4':
                    page_domain = [
                        ('view_id', 'in', dic_page_view_ids_list.get("theme_4", []))]
                elif selected_readymade_tmpl == 'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_5':
                    page_domain = [
                        ('view_id', 'in', dic_page_view_ids_list.get("theme_5", []))]   
                elif selected_readymade_tmpl == 'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_6':
                    page_domain = [
                        ('view_id', 'in', dic_page_view_ids_list.get("theme_6", []))]                        

                elif selected_readymade_tmpl == 'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_none':
                    page_domain = [
                        ('view_id', 'in', dic_page_view_ids_list.get("theme_none", []))]

                    theme_none_domain = [
                        ('view_id.key', '=', 'website.homepage'),
                        ('website_id', '=', request.website.id),
                    ]

                    page_home = request.env['website.page'].sudo().search(
                        theme_none_domain)
                    if page_home:
                        page_home.sudo().is_homepage = True

                # PUBLISH SPECIFIED THEME PAGES.
                pages = request.env['website.page'].sudo().search(
                    page_domain + multiwebsite_domain)

                ### Onemate Menus ###

                ### THEME 5

                onemate_menus_urls_readymade_5 = [ 'about2','services16','counter7','portfolio',
                                      'team77','testimonial8','hotspot9','events55',
                                      'contact85']
                    
                if selected_readymade_tmpl != "sh_corpomate_theme.sh_corpomate_theme_layout_readymade_5":
                    for rec in onemate_menus_urls_readymade_5:
                        
                        domain = [
                            ('page_id', '=', False),
                            ('url', '=', '#' +rec),
                        ]
                        search_menu = request.env['website.menu'].sudo().search(
                            domain, limit=1)
                        
                        if search_menu:
                            search_menu.sudo().unlink()
                
                if selected_readymade_tmpl == "sh_corpomate_theme.sh_corpomate_theme_layout_readymade_5":
                    domain = [('website_id', '=', request.website.id),('parent_id', '!=', False)]

                    search_menus = request.env['website.menu'].sudo().search(domain)
                    for rec in search_menus:
                        if rec:
                            rec.sudo().unlink()
                

                    for rec in onemate_menus_urls_readymade_5:
                        name = ''.join([i for i in rec if not i.isdigit()])
                        domain = [
                            ('page_id', '=', False),
                            ('url', '=', '#' +rec),
                        ]
                        search_menu = request.env['website.menu'].sudo().search(
                            domain, limit=1)
                        if not search_menu:
                            menu_vals = {
                                'page_id': False,
                                'name': name.capitalize(),
                                'url': '#' +rec,
                                'parent_id': request.website.menu_id.id,
                                'website_id': request.website.id,
                            }
                            menus = request.env['website.menu'].sudo().create(menu_vals)
                ### THEME 5
                            
                ### THEME 6
                onemate_menus_urls_readymade_6 = ['about26','counter26','service26','pricing26',
                        'testimonial26','blog26','contactus26']
                
                if selected_readymade_tmpl != "sh_corpomate_theme.sh_corpomate_theme_layout_readymade_6":
                    for rec in onemate_menus_urls_readymade_6:
                        
                        domain = [
                            ('page_id', '=', False),
                            ('url', '=', '#' +rec),
                        ]
                        search_menu = request.env['website.menu'].sudo().search(
                            domain, limit=1)
                        
                        if search_menu:
                            search_menu.sudo().unlink()
                
                if selected_readymade_tmpl == "sh_corpomate_theme.sh_corpomate_theme_layout_readymade_6":
                    domain = [('website_id', '=', request.website.id),('parent_id', '!=', False)]

                    search_menus = request.env['website.menu'].sudo().search(domain)
                    for rec in search_menus:
                        if rec:
                            rec.sudo().unlink()
                

                    for rec in onemate_menus_urls_readymade_6:
                        name = ''.join([i for i in rec if not i.isdigit()])
                        domain = [
                            ('page_id', '=', False),
                            ('url', '=', '#' +rec),
                        ]
                        search_menu = request.env['website.menu'].sudo().search(
                            domain, limit=1)
                        if not search_menu:
                            menu_vals = {
                                'page_id': False,
                                'name': name.capitalize(),
                                'url': '#' +rec,
                                'parent_id': request.website.menu_id.id,
                                'website_id': request.website.id,
                            }
                            menus = request.env['website.menu'].sudo().create(menu_vals)



                ### THEME 6                    
                ### Onemate Menus ###

                if pages and selected_readymade_tmpl != 'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_none':

                    # Create Menu Here
                    for page in pages:
                        menu_vals = {
                            'page_id': page.id,
                            'name': page.name,
                            'url': page.url,
                            'parent_id': request.website.menu_id.id,
                            'website_id': request.website.id,
                        }

                        # search menu
                        domain = [
                            ('website_id', '=', request.website.id),
                            ('page_id', '=', page.id),
                            ('url', '=', page.url),
                        ]

                        search_menu = request.env['website.menu'].sudo().search(
                            domain)
                        if not search_menu:

                            # search menu
                            domain = [
                                ('website_id', '=', False),
                                ('page_id', '=', page.id),
                                ('url', '=', page.url),
                            ]
                            search_menu = request.env['website.menu'].sudo().search(
                                domain, limit=1)

                            if search_menu:
                                # TODO: ADD HOMEPAGE AND SEQUENCE IN BELOW DICTIONARY.

                                menu_vals.update({
                                    "sh_website_mega_menu_html": search_menu.sh_website_mega_menu_html,
                                    "sequence": search_menu.sequence,
                                })

                            menus = request.env['website.menu'].sudo().create(
                                menu_vals)

                            # ========================
                            # Make Home Page Here

                            if page.view_id and 'sh_corpomate_theme.sh_corpomate_tmpl_home_' in page.view_id.key:
                                page.sudo().is_homepage = True

                        if search_menu:

                            menu_dic = {
                                "id": search_menu.id,
                                "name": search_menu.name,
                                "url": search_menu.url,
                                "new_window": search_menu.new_window,
                                "is_mega_menu": search_menu.is_mega_menu,
                                "sequence": search_menu.sequence,
                                "parent_id": search_menu.parent_id.id if search_menu.parent_id else False
                            }

                            list_keep_menu_data_dic.append(menu_dic)


                # ======================================================
                # STEP 3 SHOW SELECTED THEME PAGES
                # ======================================================

        # ==============================================================
        # FOR READYMADE THEME
        # ==============================================================

        response = super(Website_odoo16, self).theme_customize_data(
            is_view_data, enable, disable, reset_view_arch)

        return response


class main(http.Controller):

    #################################
    # Our partner with categories
    #################################
    @http.route('/sh_corpomate_theme/our_partner_get_categories', type='json', auth="none", methods=['post'], website=False)
    def our_partner_get_categories(self, item_template=False, categs_ids=False):
        data = ''
        list_categ_ids = []
        categories = False
        if categs_ids:
            for categ_id in categs_ids:
                if type(categ_id) != int:
                    categ_id = int(categ_id)
                list_categ_ids.append(categ_id)

        if list_categ_ids:
            categories = request.env['sh.corpomate.theme.our.partner.category'].sudo(
            ).search([('id', 'in', list_categ_ids)])

        if categories and item_template:
            list_partners = []
            our_partners = request.env['sh.corpomate.theme.our.partner']

            for category in categories:

                domain = [
                    ('active', '=', True),
                    ('category_id', '=', category.id),
                ]
                partners = our_partners.sudo().search(
                    domain)
                if partners:
                    list_partners += partners
            data = request.env["ir.ui.view"].sudo()._render_template(item_template, values={
                'sh_our_partners': list_partners,
            })
        values = {
            'data': data,
        }

        return values
    #################################
    # Our partner with categories
    #################################

    @http.route('/sh_corpomate_theme/render_testimonial', type='json', auth="none", methods=['post'], website=True)
    def render_testimonial(self, template_id=False):
        domain_testimonial = [
            ('active', '=', True),
            ('website_id', 'in', (False, request.website.id))
        ]

        testimonial_order = "sequence desc"

        testimonials = request.env['sh.corpomate.theme.testimonial'].sudo().search(
            domain_testimonial,
            order=testimonial_order,
        )

        data = Markup('<div class="owl-carousel owl-theme">')
        if testimonials:
            for testimonial in testimonials:
                data += request.env["ir.ui.view"]._render_template(template_id, values={
                    'testimonial': testimonial,
                })
        data = data + Markup('</div>')
        return data

    @http.route('/sh_testimonial_snippet/get_testimonial', type='json', auth='public', website=True)
    def get_testimonial(self, item_template=False, **kwargs):
        Testimonials = request.env['sh.corpomate.theme.testimonial'].sudo()
        res = {}
        domain = [('active', '=', True)]
        tests = Testimonials.search(domain)

        if tests:
            res.update({
                'testimonials': tests
            })

        data = request.env["ir.ui.view"].sudo(
        )._render_template(item_template, values=res)

        values = {
            'data': data
        }

        return values
