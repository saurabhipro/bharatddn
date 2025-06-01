# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo.http import request
from odoo import http
import uuid
import json
from datetime import datetime

from odoo.osv import expression
from ast import literal_eval
# from odoo.addons.http_routing.models.ir_http import slug


def generate_slider_tab_token():
    ran_num = str(uuid.uuid4().int)
    token = int(ran_num[:5] + ran_num[-5:])
    return str(token)


class Main(http.Controller):

    # --------------------------------------------------------------------------
    # Prepare Products Vals
    # --------------------------------------------------------------------------

    def _prepare_blog_post_vals(self, posts):
        fields = ['id', 'name', 'cover_properties', 'post_date', 'subtitle']
        res = {}
        res.update({
            'posts': posts.read(fields),
        })
        slug = request.env['ir.http']._slug
        for res_post, post in zip(res['posts'], posts):
            cover_properties = json.loads(post.cover_properties)
            dt = datetime.date(post.post_date)
            post_date_month_name = dt.strftime("%B")
            post_date_month_name_short = dt.strftime("%b")
            post_date_month_day = dt.strftime("%d")
            post_date = dt.strftime("%d %B %Y")
            # post_url = f'/blog/{post.blog_id}/post/{post}'
            post_url = '/blog/%s/%s' % (slug(post.blog_id), slug(post))

            res_post['cover_properties'] = cover_properties
            res_post['post_date'] = post_date
            res_post['post_url'] = post_url
            res_post['img_src'] = cover_properties.get(
                'background-image', False)
            res_post['post_date_month_name'] = post_date_month_name
            res_post['post_date_month_name_short'] = post_date_month_name_short
            res_post['post_date_month_day'] = post_date_month_day

        return res.get('posts')

    # --------------------------------------------------------------------------
    # Prepare Products Vals
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Get Products
    # --------------------------------------------------------------------------

    @http.route('/sh_blog_filter_snippet/get_posts', type='json', auth='public', website=True)
    def get_posts(self, item_template=False, blogs_ids=False, filter_id=False, options={}, **kwargs):
        BlogPosts = request.env['blog.post']
        res = {}
        data = ''
        filter = False

        # --------------------------------------------------------------------------
        # Make Domain

        # --------------------------------------------------------------------------
        # Prepare Options
        order = options.get('order', "published_date desc")
        limit = options.get('limit', False)

        # --------------------------------------------------------------------------
        # Prepare domain and order from filters
        if filter_id:
            default_domain = [
                ('website_published', '=', True),
            ] + request.website.website_domain()

            filter = request.env['sh.blog.filter.snippet'].sudo().search(
                [('id', '=', filter_id)], limit=1)

        # Default Behavior
        is_show_tab_local = True
        is_show_slider_local = False
        if filter:
            is_show_tab_local = filter.is_show_tab
            is_show_slider_local = filter.is_show_slider

        # ========================================
        # Prepare Tabs
        # ========================================
        list_tabs_dic = []
        tab_token_pair_dic = {}

        if filter and filter.tab_blog_post_line:
            for tab in filter.tab_blog_post_line:
                token = generate_slider_tab_token()
                nav_tab_dic = {
                    'id': tab.id,
                    'name': tab.name,
                    'href': '#nav_tab_' + token
                }

                list_tabs_dic.append(nav_tab_dic)
                tab_token_pair_dic.update({
                    tab.id: token
                })

        # ========================================
        # Prepare Tabs
        # ========================================

        # ========================================
        # Prepare Tab pane/ Tab Content
        # ========================================
        list_tab_panes_dic = []
        if filter and filter.tab_blog_post_line:
            is_first_tab_with_content = True
            tabs = filter.tab_blog_post_line

            # ---------------------------
            # FOR SINGLE TAB
            # ---------------------------
            if options.get('tab_id', False):
                tab_id = options.get('tab_id')
                tabs = filter.tab_blog_post_line.filtered(
                    lambda line: line.id == tab_id)
            # ---------------------------
            # FOR SINGLE TAB
            # ---------------------------

            for tab in tabs:
                tab_pane_dic = {
                    'id': tab.id,
                    'name': tab.name,
                    'id_tab_pane': 'nav_tab_' + tab_token_pair_dic.get(tab.id)
                }

                tab_content = []
                if is_first_tab_with_content and filter.filter_type == 'manual' and tab.blog_post_ids:
                    tab_content = self._prepare_blog_post_vals(
                        tab.blog_post_ids)

                elif is_first_tab_with_content and filter.filter_type == 'domain':
                    # --------------------------------------------------------------------------
                    # Prepare domain and order from filters
                    if tab.filter_id.sudo():
                        default_domain = [
                            ('website_published', '=', True),
                        ] + request.website.website_domain()

                        filter_sudo = tab.filter_id.sudo()
                        domain = filter_sudo._get_eval_domain()
                        domain = expression.AND([domain, default_domain])
                        order = ','.join(literal_eval(
                            filter_sudo.sort)) or 'published_date desc'

                        limit = None
                        if tab.limit > 0:
                            limit = tab.limit

                        # --------------------------------------------------------------------------
                        # Find Products
                        posts = BlogPosts.search(
                            domain,
                            limit=limit,
                            order=order
                        )
                        if posts:
                            tab_content = self._prepare_blog_post_vals(posts)

                tab_pane_dic.update({
                    'list_posts_dic': tab_content
                })

                # ==================================
                # No TAB THINGS
                if is_show_tab_local:
                    is_first_tab_with_content = False
                else:
                    is_first_tab_with_content = True

                # No TAB THINGS
                # ==================================
                list_tab_panes_dic.append(tab_pane_dic)

        # ==================================
        # NO TAB THINGS
        if not is_show_tab_local and list_tab_panes_dic:
            list_tab_panes_dic_single = list_tab_panes_dic[0]
            list_posts_dic_single_tab = []
            for tab_pane_dic in list_tab_panes_dic:
                list_posts_dic = tab_pane_dic.get("list_posts_dic", [])
                for posts_dic in list_posts_dic:
                    list_posts_dic_single_tab.append(posts_dic)

            list_tab_panes_dic_single.update({
                'list_posts_dic': list_posts_dic_single_tab,
            })

            list_tab_panes_dic = [list_tab_panes_dic_single]
            list_tabs_dic = []

        res.update({
            'list_tabs_dic': list_tabs_dic,
            'list_tab_panes_dic': list_tab_panes_dic,
            'row_classes': 'owl-carousel owl-theme' if is_show_slider_local else 'row',
            'column_classes': 'item' if is_show_slider_local else options.get('column_class', 'col-md-4')
        })

        if item_template:
            data = request.env["ir.ui.view"].sudo(
            )._render_template(item_template, values=res)

        values = {
            'data': data
        }

        if filter:
            values.update({
                'items':    filter.items,
                'autoplay': filter.autoplay,
                'speed':    filter.speed,
                'loop':     filter.loop,
                'nav':      filter.nav,
                'is_show_slider_local': is_show_slider_local,
            })

        return values
