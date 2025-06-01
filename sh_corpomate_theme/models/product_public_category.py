# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class ProductPublicCategory(models.Model):
    _inherit = "product.public.category"

    sh_mega_menu_img = fields.Binary(string="Category Mega Menu Image")
