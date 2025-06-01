# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models, _
from odoo.tools import is_html_empty

class ShWebsiteStoreTags(models.Model):
    _name = 'sh.website.store.tags'
    _description = 'Website Store Tags'

    name = fields.Char('Name')
    color = fields.Integer('Color Index', default=1)