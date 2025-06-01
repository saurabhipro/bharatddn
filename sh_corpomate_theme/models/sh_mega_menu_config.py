# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class MegaMenuConfig(models.Model):
    _name = "sh.mega.menu.config"
    _description = "Mega Menu Config"
    _order = "id desc"

    name = fields.Char(string="Name")
    style = fields.Selection([('style_1', 'Style 1'), ('style_2', 'Style 2')], string="Style (Snippet Number)")

    categ_line = fields.One2many(
        comodel_name="sh.mega.menu.config.categ.line", inverse_name="mega_menu_id")
