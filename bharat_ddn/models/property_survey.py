from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SurveyParameters(models.Model):
    _name = 'ddn.property.survey'
    _description = 'Survey Parameters'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'property_id'
    
    unit = fields.Char('Unit')
    property_id = fields.Many2one('ddn.property.info', 'Property ID', required=True)
    company_id = fields.Many2one('res.company', string="Company", related='property_id.company_id', store=True, default=lambda self : self.env.company.id, readonly=True)
    address_line_1 = fields.Char('Address Line 1', required=True)
    address_line_2 = fields.Char('Address Line 2')
    house_number = fields.Char('House Number')
    total_floors = fields.Char('Total Floors')
    floor_number = fields.Char('Floor Number')
    owner_name = fields.Char('Owner Name')
    father_name = fields.Char('Father Name')
    area = fields.Float('Area (in Sq. Ft.)')
    area_code = fields.Char('Area Code')
    latitude = fields.Char('Latitude')
    longitude = fields.Char('Longitude')
    surveyer_id = fields.Many2one('res.users', string='Surveyor')
    installer_id = fields.Many2one('res.users', string='Installer')
    property_image = fields.Binary() 
    property_image1 = fields.Binary() 
    mobile_no = fields.Char('Mobile No')

    @api.onchange('property_id')
    def _onchange_property_id(self):
        if self.property_id:
            self.address_line_1 = self.property_id.address_line_1
            self.address_line_2 = self.property_id.address_line_2
            self.house_number = self.property_id.house_number
            self.owner_name = self.property_id.owner_name
            self.mobile_no = self.property_id.mobile_no
            self.longitude = self.property_id.longitude
            self.latitude = self.property_id.latitude
            self.surveyer_id = self.property_id.surveyer_id

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            if record.property_id:
                # Update property with all relevant survey fields
                vals_to_write = {}
                if record.latitude:
                    vals_to_write['latitude'] = record.latitude
                if record.longitude:
                    vals_to_write['longitude'] = record.longitude
                if record.mobile_no:
                    vals_to_write['mobile_no'] = record.mobile_no
                if record.surveyer_id:
                    vals_to_write['surveyer_id'] = record.surveyer_id.id
                if record.address_line_1:
                    vals_to_write['address_line_1'] = record.address_line_1
                if record.address_line_2:
                    vals_to_write['address_line_2'] = record.address_line_2
                if record.house_number:
                    vals_to_write['house_number'] = record.house_number
                if record.owner_name:
                    vals_to_write['owner_name'] = record.owner_name
                if vals_to_write:
                    record.property_id.write(vals_to_write)
        return records

    def write(self, vals):
        res = super().write(vals)
        for record in self:
            if record.property_id:
                vals_to_write = {}
                # Update all relevant fields in property when changed in survey
                if 'latitude' in vals and record.latitude:
                    vals_to_write['latitude'] = record.latitude
                if 'longitude' in vals and record.longitude:
                    vals_to_write['longitude'] = record.longitude
                if 'mobile_no' in vals and record.mobile_no:
                    vals_to_write['mobile_no'] = record.mobile_no
                if 'surveyer_id' in vals and record.surveyer_id:
                    vals_to_write['surveyer_id'] = record.surveyer_id.id
                if 'address_line_1' in vals and record.address_line_1:
                    vals_to_write['address_line_1'] = record.address_line_1
                if 'address_line_2' in vals and record.address_line_2:
                    vals_to_write['address_line_2'] = record.address_line_2
                if 'house_number' in vals and record.house_number:
                    vals_to_write['house_number'] = record.house_number
                if 'owner_name' in vals and record.owner_name:
                    vals_to_write['owner_name'] = record.owner_name
                if vals_to_write:
                    record.property_id.write(vals_to_write)
        return res




    