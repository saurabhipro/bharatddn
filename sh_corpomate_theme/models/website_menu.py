# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, _, fields
from odoo.exceptions import UserError
from odoo.tools.translate import html_translate


class WebsiteMenu(models.Model):
    _inherit = "website.menu"

    sh_website_mega_menu_html = fields.Html(string = "Mega Menu", translate = html_translate)

    # method which redirect to frontend for design menu html structure
    def action_sh_design_mega_menu(self, context=None):

        if not len(self.ids) == 1:
            raise UserError(
                _('You can only design only one mega menu at a time.'))

        url = f'/sh_website_megamenu/design_mega_menu?menu_id={self.id}&enable_editor=1'
        return {'name': ('Edit Mega Menu'),
                'type': 'ir.actions.act_url',
                'url': url,
                'target': 'new'}
