# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import  http, _
import pytz
from datetime import datetime
from odoo.http import request

class WebsiteGetTz(http.Controller):

    @http.route(['/current/timezone'], type='json', auth="public", website=True)
    def get_current_timezone(self,tz,launch_date):

        # for convert launch date to datetime formate
        date_format = "%Y-%m-%d %H:%M:%S"
        launch_date_date = datetime.strptime(launch_date, date_format)

        # conver time to timezone
        converted_launch_date = launch_date_date.replace(tzinfo=pytz.UTC).astimezone(pytz.timezone(tz or 'UTC'))

        return converted_launch_date
    

    @http.route(['/website/configuration'], type='json', auth="public", website=True)
    def lauch_timer_end(self):
        website_id = request.website
        if website_id:
            website_id.sudo().sh_website_coming_soon_is_coming_soon = False
