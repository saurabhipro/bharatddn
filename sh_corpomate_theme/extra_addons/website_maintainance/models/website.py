# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    is_wm_maintainance = fields.Boolean(string="Maintainance")
    sh_wm_titile = fields.Char(string="Title ", translate=True)
    sh_wm_message = fields.Text(string="Message ", translate=True)
    sh_wm_email = fields.Char(string="E-Mail")
