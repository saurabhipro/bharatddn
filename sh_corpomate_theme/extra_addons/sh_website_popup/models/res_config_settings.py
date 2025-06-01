# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
from odoo.tools.translate import html_translate


class WebisteConfiguration(models.TransientModel):
    _inherit = 'res.config.settings'

    swp_is_popup_msg = fields.Boolean(related='website_id.swp_is_popup_msg',
                                      string="swp popup Message",
                                      readonly=False)
    swp_titile = fields.Char(related="website_id.swp_titile",
                             string="popup Title",
                             readonly=False)
    swp_message = fields.Html(related="website_id.swp_message",
                              string="popup Message",
                              readonly=False)
    swp_link_btn_name = fields.Char(related="website_id.swp_link_btn_name",
                                    string="popup Link Button Name",
                                    readonly=False)
    swp_link_url = fields.Char(related="website_id.swp_link_url",
                               string="popup Link URL",
                               readonly=False)
    swp_banner_img = fields.Image(related="website_id.swp_banner_img",
                                  string="popup Image",
                                  readonly=False)

    # New popup style
    swp_popup_style = fields.Selection(related='website_id.swp_popup_style',
                                       string="swp popup Style",
                                       readonly=False)

    sh_website_popup_limit_days = fields.Integer(
        related='website_id.sh_website_popup_limit_days',
        string="Hide for",
        readonly=False)
    sh_website_popup_website_page_ids = fields.Many2many(
        string="Show On",
        comodel_name="website.page",
        related="website_id.sh_website_popup_website_page_ids",
        readonly=False,
    )


class Website(models.Model):
    _inherit = 'website'

    swp_is_popup_msg = fields.Boolean(string="swp popup Message")
    swp_titile = fields.Char(string="popup Title", translate=True)
    swp_message = fields.Html(string="popup Message", translate=html_translate)
    swp_link_btn_name = fields.Char(string="popup Link Button Name",
                                    translate=True)
    swp_link_url = fields.Char(string="popup Link URL")
    swp_banner_img = fields.Image(string="popup Image")

    # New popup style
    swp_popup_style = fields.Selection(
        [
            ('style_1', 'Style 1'),
            ('style_2', 'Style 2'),
            ('style_3', 'Style 3'),
            ('style_4', 'Style 4'),
            ('style_5', 'Style 5'),
        ],
        default="style_1",
        string="popup Style",
    )

    sh_website_popup_limit_days = fields.Integer(string='Hide for')

    sh_website_popup_website_page_ids = fields.Many2many(
        string="Show On",
        comodel_name="website.page",
    )
