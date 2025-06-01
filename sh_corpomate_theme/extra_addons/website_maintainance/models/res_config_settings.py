# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class WebisteConfiguration(models.TransientModel):
    _inherit = "res.config.settings"

    is_wm_maintainance = fields.Boolean(
        related="website_id.is_wm_maintainance",
        string="Maintainance",
        readonly=False
    )
    sh_wm_titile = fields.Char(
        related="website_id.sh_wm_titile",
        string="Title ",
        readonly=False
    )
    sh_wm_message = fields.Text(
        related="website_id.sh_wm_message",
        string="Message ",
        readonly=False
    )
    sh_wm_email = fields.Char(
        related="website_id.sh_wm_email",
        string="E-Mail",
        readonly=False
    )
