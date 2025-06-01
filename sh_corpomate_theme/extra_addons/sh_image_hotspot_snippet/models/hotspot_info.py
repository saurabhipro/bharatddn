# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.


from odoo import fields, models, _
from odoo.exceptions import UserError
from odoo.tools.translate import html_translate


class ShImageHotspotInfo(models.Model):
    _name = "sh.image.hotpost.info"
    _description = "Hotpost Info"

    name = fields.Char('Name', required=True)
    active = fields.Boolean('Active', default=True)
    description = fields.Html('description', translate=html_translate)

    def action_sh_design_popover(self, context=None):
        """
            CUSTOM METHOD BY SOFTHEALER TECHNOLOGIES
            method which redirect to frontend for design menu html structure
        """
        if not len(self.ids) == 1:
            raise UserError(
                _('You can only design only one mega menu at a time.'))

        url = '/sh_image_hotspot_snippet/design_popover?id=%d&enable_editor=1' % (
            self.id)
        return {
            'name': _('Edit Popover'),
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }
