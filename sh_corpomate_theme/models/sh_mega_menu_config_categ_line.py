# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class SliderTabProductLine(models.Model):
    _name = "sh.mega.menu.config.categ.line"
    _description = "Mega Menu Config Category Line"
    _order = "sequence"

    sequence = fields.Integer(string='Sequence')
    category_id = fields.Many2one(
        comodel_name="product.public.category", string="Main Category", required=True)
    sub_category_ids = fields.Many2many(
        comodel_name="product.public.category", string="Sub categories")

    mega_menu_id = fields.Many2one(comodel_name="sh.mega.menu.config",
                                   string="Mega Menu Reference", required=True, ondelete='cascade')

    product_ids = fields.Many2many(
        comodel_name="product.template", string="Products")
