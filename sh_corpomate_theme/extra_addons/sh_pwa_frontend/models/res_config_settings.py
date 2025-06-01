from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    enable_web_push_notification = fields.Boolean(
        "Enable Web Push Notification")
    api_key = fields.Char("Api Key")
    vapid = fields.Char("Vapid", readonly=False)
    config_details = fields.Text("Config Details")


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    enable_web_push_notification = fields.Boolean(
        related='company_id.enable_web_push_notification', readonly=False)
    api_key = fields.Char(related='company_id.api_key', readonly=False)
    vapid = fields.Char(related='company_id.vapid', readonly=False)
    config_details = fields.Text(
        related='company_id.config_details', readonly=False)
