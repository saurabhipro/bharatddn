from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResUsers(models.Model):
    _inherit = "res.users"

    zone_no = fields.Many2one('ddn.zone', string='Zone No')
    ward_no = fields.Many2many('ddn.ward',string='Ward No')
    is_surveyor = fields.Boolean(string='Is Surveyor')
    mobile = fields.Char(string="Mobile")


    @api.constrains('mobile')
    def _check_unique_mobile(self):
        for rec in self:
            if rec.mobile:
                existing_user = self.search([('mobile', '=', rec.mobile), ('id', '!=', rec.id)], limit=1)
                if existing_user:
                    raise ValidationError(f"The mobile number {rec.mobile} is already used by another user.")
           

