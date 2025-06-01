# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo.osv import expression
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from math import radians, sin, cos, acos



class ShWebsiteStoreLocator(http.Controller):

    @http.route(['/sh_get_store_details_template'], type='json', auth='public', website=True)
    def sh_get_store_details_template(self, **post):
        store_id = post.get('StoreId', False)

        fields = ['id', 'name', 'sh_street', 'sh_street2', 'sh_zip', 'sh_city', 'sh_days_from', 'sh_days_to',
                  'sh_contact_name', 'sh_contact_mobile', 'sh_contact_phone', 'sh_contact_email',
                  'sh_contact_fax', 'sh_contact_website']
        
        if store_id in ['', "", False, 0]:
            store_id = False
        else:
            store_id = int(store_id)

        if store_id:
            store_id = request.env['sh.website.store.locator'].sudo().browse(store_id)

            data = {'stores':store_id.read(fields)}
            if store_id:
                if store_id.sh_store_tag_ids:
                    tag_names = store_id.sh_store_tag_ids.mapped('name')

                    data.get('stores')[0].update({
                        'tag_names':tag_names,
                    })
                if store_id.sh_state_id:
                    data.get('stores')[0].update({
                        'state':store_id.sh_state_id.name,
                    })
                if store_id.sh_country_id:
                    
                    data.get('stores')[0].update({
                        'country':store_id.sh_country_id.name,
                    })
                if store_id.sh_time_from:
                    sh_time_from = '{0:02.0f}:{1:02.0f}'.format(*divmod(store_id.sh_time_from * 60, 60))
                    data.get('stores')[0].update({
                        'sh_time_from':sh_time_from,
                    })
                
                if store_id.sh_time_to:
                    sh_time_to = '{0:02.0f}:{1:02.0f}'.format(*divmod(store_id.sh_time_to * 60, 60))
                    data.get('stores')[0].update({
                        'sh_time_to':sh_time_to,
                    })

            return data
        return {}

    @http.route(['/sh_get_google_api_key'], type='json', auth="public", website=True)
    def sh_get_google_api_key(self, **post):
        """
        GET GOOGLE API KEY
        """
        Website = request.env['website']
        api_key = False
        website_api_key = Website.get_current_website().google_maps_api_key
        if website_api_key:
            api_key = website_api_key
        return {'api_key': api_key}
    
    # custom controller to get country and state id from names
    @http.route(['/sh_get_country_state_code'], type='json', auth="public", website=True)
    def sh_get_country_state_code(self, country_name='', state_name='', **post):
        country_name = country_name or ''
        state_name = state_name or ''
        code = ''

        country_code = request.env["res.country"].sudo().search(
            [('name', '=', country_name)], limit=1)
        if country_code:
            code = country_code.id if country_code else ''
            country_name = country_code.name if country_code else ''

        state_code = request.env["res.country.state"].sudo().search(
            [('name', '=', state_name)], limit=1)
        if state_code:
            state_name = state_code.name if state_code else ''
            state_code = state_code.id if state_code else ''
        return {
            'country_code': code or False,
            'country_name': country_name or '',
            'state_code': state_code or False,
            'state_name': state_name or ''
        }
    
    @http.route(["/store/sh_store_locator/vals"], type='json', auth="public", website=True)
    def store_locator_vals(self, **post):
        domain = [('active', '=', True)]

        sale_store_obj = request.env['sh.website.store.locator'].sudo()

        key, sum_lat, sum_lng, store_dict, vals = 0, 0, 0, {}, {}

        Website = request.env['website']
        google_api_key = Website.get_current_website().google_maps_api_key
        if google_api_key:
            vals.update({
                'google_api_key':google_api_key,
            })
        
        store_ids = sale_store_obj.search(domain)

        if store_ids:
            for store in store_ids:
                if store.sh_latitude and store.sh_longitude:
                    store_dict.update(self.get_store_data_dict(store, key))
                    sum_lat = sum_lat + float(store.sh_latitude)
                    sum_lng = sum_lng + float(store.sh_longitude)
                    key = key + 1

            if key != 0:
                cen_lat, cen_lng, value = sum_lat/key, sum_lng/key, self.get_map_config()
                if not value.get('auto'):
                    cen_lat, cen_lng = value.get('cen_lat'), value.get('cen_lng')
                zoom, map_type = value.get('zoom'), value.get('type')
                vals.update({'map_init_data': {'map_center_lat': cen_lat,
                                               'map_center_lng': cen_lng,
                                               'map_zoom':  int(zoom),
                                               'map_type': str(map_type)
                                               },
                             'map_stores_data': store_dict,
                             'map_search_radius': value.get('search_radius'),
                             })
                
                return vals
            else:
                return False
            
    @http.route(["/store/sh_store_locator"], type='http', auth="public", website=True)
    def sh_website_store_locator_page(self, **kw):
        vals = {}
        sale_store_obj = request.env['sh.website.store.locator'].sudo()
        sale_state_obj = request.env['res.country.state'].sudo()
        sale_country_obj = request.env['res.country'].sudo()
        
        domain = [('active', '=', True)]
        store_ids = sale_store_obj.search(domain)
        if store_ids:
            vals.update({
                'store_ids':store_ids
            })

        if store_ids and store_ids.filtered(lambda rec: rec.sh_state_id).mapped('sh_state_id'):
            states = store_ids.filtered(lambda rec: rec.sh_state_id).mapped('sh_state_id').ids
            state_list = []
            for rec in states:
                state = sale_state_obj.browse(rec)
                state_list.append(state.name)
            
            if state_list:
                vals.update({
                    'store_filter_states':state_list,
                })

        if store_ids and store_ids.filtered(lambda rec: rec.sh_country_id).mapped('sh_country_id'):
            countries = store_ids.filtered(lambda rec: rec.sh_country_id).mapped('sh_country_id').ids
            country_list = []
            for rec in countries:
                country = sale_country_obj.browse(rec)
                country_list.append(country.name)
            
            if country_list:
                vals.update({
                    'store_filter_countries':country_list
                })
        return request.render("sh_corpomate_theme.sh_website_store_locator_page", vals)
    
    def get_store_data_dict(self, store=None, key=None):
        data = {key: {'store_lat': store.sh_latitude,
                      'store_lng': store.sh_longitude,
                      'store_name': store.name,
                      'store_image': False if not store.sh_store_img else request.website.image_url(store, 'sh_store_img'),
                      'store_address': [store.sh_street, store.sh_city, store.sh_state_id.name, store.sh_country_id.name, store.sh_zip, store.sh_contact_phone, store.sh_contact_mobile, store.sh_contact_fax, store.sh_contact_email, store.sh_contact_website],
                      'store_id': store.id,
                      'store_city':store.sh_city,
                      'store_state':store.sh_state_id.name,
                      'store_country':store.sh_country_id.name,
                      'store_day_start':store.sh_days_from,
                      'store_day_end':store.sh_days_to, 
                      'sh_time_from':'{0:02.0f}:{1:02.0f}'.format(*divmod(store.sh_time_from * 60, 60)),
                      'sh_time_to':'{0:02.0f}:{1:02.0f}'.format(*divmod(store.sh_time_to * 60, 60)),
                      'sh_store_tag_ids':store.sh_store_tag_ids.mapped('name'),
                      }
                }
        return data
    
    def get_map_config(self):
        vals = {'auto': True, 'zoom': 5, 'type': 'satellite'}
        res = self.get_locator_config_settings_values()
        if res.get('map_center') == 'manually' and res.get('map_lat') and res.get('map_long'):
            vals['auto'] = False
            vals.update({'cen_lat': res.get('map_lat'),
                         'cen_lng': res.get('map_long')})
        if res.get('map_zoom'):
            vals['zoom'] = res.get('map_zoom')
        if res.get('map_type'):
            vals['type'] = res.get('map_type')
        vals['search_radius'] = res.get(
            'search_radius') if res.get('search_radius') else 50
        return vals
    
    def get_locator_config_settings_values(self):
        """ this function retrn all configuration value for website stock locator module."""

        sh_map_zoom = request.website.sh_map_zoom
        res = {
            'map_center' : 'auto',
            'manually_option' : 'address',
            'map_lat' : 0.00,
            'map_long' : 0.00,
            'map_zoom' :sh_map_zoom,
            'map_type' : 'roadmap',
            'search_radius' : 5000,
            'google_api_key' : request.website.google_maps_api_key if request.website.google_maps_api_key else '',
        }
        
        return res
    
    
    @http.route(["/store/sh_store_locator/current_location"], type='json', auth="public", website=True)
    def get_current_location(self, **post):

        current_latitude = post.get('current_latitude','')
        current_longitude = post.get('current_longitude','')

        sh_current_latitude = radians(float(current_latitude))
        sh_current_longitude = radians(float(current_longitude))

        sale_store_obj = request.env['sh.website.store.locator'].sudo()
        domain = [('active', '=', True)]
        store_ids = sale_store_obj.search(domain)

        key, dist_dic = 0, {}#, []

        if store_ids:
            for rec in store_ids:
                if rec.sh_latitude and rec.sh_longitude:
                    sh_latitude = radians(float(rec.sh_latitude))
                    sh_longitude = radians(float(rec.sh_longitude))
                    dist = int(6371.01 * acos(sin(sh_current_latitude)*sin(sh_latitude) + cos(sh_current_latitude)*cos(sh_latitude)*cos(sh_current_longitude - sh_longitude)))
                    dist_dic.update(self.get_store_dist_dict(rec, dist, key))
                    key = key + 1
        if dist_dic:
            store_with_smallest_dist = min(dist_dic.values(), key=lambda x: x['store_dist'])
            return store_with_smallest_dist
        else:
            return []
    
    def get_store_dist_dict(self, rec=None, dist=None,key=None,):
        data = {key :{
            'store_name':rec.name,
            'store_dist':dist,
        }}
        return data
