from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.utils import ensure_db, _get_login_redirect_url, is_user_internal
import pandas as pd
from io import BytesIO
import logging
_logger = logging.getLogger(__name__)

class CustomWebsite(http.Controller):
    
    @http.route('/get/<string:uuid>', auth='none', website=True)
    def get_property_details_by_uuid(self, uuid, **kw):
        # print("UPIC No:", uuid)

        property = request.env['ddn.property.info'].sudo().search([('uuid', '=', uuid)], limit=1)
        print("property - ", property.colony_id.name)

        if not property:
            # return request.render('web.404')
            return "No property found"

        # This loop is unnecessary because 'property' is a single record (limit=1)
        if property.survey_line_ids:
            print("Property Survey Line:", property.survey_line_ids[0])
        else:
            print("Property: No survey lines found")

        return request.render('microsite.id_indore_microsite_template', {'property':property})
