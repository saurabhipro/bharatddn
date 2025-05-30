from odoo import models, fields, api
from odoo.exceptions import ValidationError
import base64
import re
from io import BytesIO
try:
    import qrcode
except ImportError:
    qrcode = None  # If not installed, you'll need to pip install qrcode[pil]

import uuid
import qrcode
from io import BytesIO
import base64
from odoo.http import request

class PropertyInfo(models.Model):
    _name = 'ddn.property.info'
    _description = 'Property Information'
    _inherit = ['mail.thread', 'mail.activity.mixin']    
    _rec_name = "upic_no"

    # Owner Information
    qr_code = fields.Binary("QR Code", compute="_compute_qr_code", store=True)
    colony_id = fields.Many2one('ddn.colony', string='Colony')
    property_status = fields.Selection([
        ('uploaded','Uploaded'),
        ('pdf_downloaded','PDF Downloaded'),
        ('surveyed', 'Surveyed'),
        ('discovered', 'Discovered')
         ], string="Property Status", default="uploaded")
    
    owner_id = fields.Char('Owner ID')
    upic_no = fields.Char('UPIC NO')
    # zone_id = fields.Many2one('ddn.zone', string='Zone', tracking=True)
    company_id = fields.Many2one('res.company', string="Company", default=lambda self : self.env.company.id, readonly=True)
    _sql_constraints = [
        ('unique_upic_no', 'UNIQUE(upic_no)', 'The UPICNO must be unique.')
    ]

    uuid = fields.Char(string='UUID', readonly=True, copy=False, default=lambda self: str(uuid.uuid4()))

    @api.depends('uuid')
    def _compute_qr_code(self):
        for record in self:
            if record.uuid:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                base_url = request.httprequest.host_url
                full_url = f"{base_url}get/property-details/{record.uuid}"
                qr.add_data(full_url)

               
                qr.make(fit=True)
                img = qr.make_image(fill='black', back_color='white')

                buffer = BytesIO()
                img.save(buffer, format='PNG')
                qr_image = base64.b64encode(buffer.getvalue())
                buffer.close()
                record.qr_code = qr_image
            else:
                record.qr_code = False

    survey_line_ids = fields.One2many('ddn.property.survey', 'property_id', string="Survey Line")

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to validate coordinates before saving."""
        for vals in vals_list:
            try:
                if vals.get('latitude'):
                    lat = vals['latitude']
                    if not re.match(r'^\d{1,2}°\s*\d{1,2}\'\s*\d{1,2}(\.\d+)?"\s*[NS]$', lat):
                        vals['latitude'] = None
                if vals.get('longitude'):
                    lng = vals['longitude']
                    if not re.match(r'^\d{1,3}°\s*\d{1,2}\'\s*\d{1,2}(\.\d+)?"\s*[EW]$', lng):
                        vals['longitude'] = None
            except (ValueError, TypeError):
                vals['latitude'] = None
                vals['longitude'] = None
        return super().create(vals_list)
    
    address_line_1 = fields.Char(string="Address 1")
    address_line_2 = fields.Char(string="Address 2")
    colony_name = fields.Char(string="Colony Name")
    house_number = fields.Char(string="H.No")
    surveyer_id = fields.Many2one('res.users', string="Surveyor")
    
    # Zone and Ward Information
    # zone = fields.Char('Zone')
    zone_no = fields.Many2one('ddn.zone', string='Zone No')
    ward_no = fields.Many2one('ddn.ward',string='Ward No')
    property_no = fields.Char('Property No')
    partition_no = fields.Char('Partition No')
    city_survey_no = fields.Char('CityServey No')
    plot_no = fields.Char('Plot No')
    old_zone_no = fields.Char('Old Zone No')
    old_ward_no = fields.Char('Old Ward No')
    old_property_no = fields.Char('Old Property No')
    unit_no = fields.Char('Unit No.')
    
    # Billing Information
    bill_no = fields.Char('Bill No')
    property_description = fields.Text('Property Description')
    
    # Plot Information
    plot_area = fields.Float('Plot Area')  # In Sq. Ft. or desired unit
    mobile_no = fields.Char('Mobile No')
    
    # Old Rent Information
    old_rental_value = fields.Float('Old Rental Value')
    old_rv = fields.Float('Old RV')
    old_property_tax = fields.Float('Old Property Tax')
    old_total_tax = fields.Float('Old Total Tax')
    
    # New Property Information
    toilet_no = fields.Char('New Toilet No')
    plot_taxable_area_sqft = fields.Char('Plot Taxable Area SqFt')
    
    owner_name = fields.Char('Owner Name')
    renter_name = fields.Char('Renter Name')
    occupier_name = fields.Char('Occupier Name')
    owner_patta = fields.Char('Owner Patta')
    owner_dukan_imarate_nav = fields.Char('Owner Dukan Imarate Nav')
    owner_dukan_flat_no = fields.Char('Owner Dukan Flat No')
    
    # Remarks
    comb_prop_remark = fields.Text('Comb Prop Remark')
    
    # Location Information
    latitude = fields.Char(
        string='Latitude',
        help='Format: DD° MM\' SS.SSS" N/S (e.g., 16° 51\' 50.003" N)'
    )
    longitude = fields.Char(
        string='Longitude',
        help='Format: DD° MM\' SS.SSS" E/W (e.g., 74° 37\' 20.926" E)'
    )
    
    @api.constrains('latitude', 'longitude')
    def _check_coordinates(self):
        print("self.env ---- ", self.env.company.name)
        """Validate DMS coordinate format"""
        for record in self:
            if record.latitude:
                if not re.match(r'^\d{1,2}°\s*\d{1,2}\'\s*\d{1,2}(\.\d+)?"\s*[NS]$', record.latitude):
                    raise ValidationError('Invalid latitude format. Use format: DD° MM\' SS.SSS" N/S')
            if record.longitude:
                if not re.match(r'^\d{1,3}°\s*\d{1,2}\'\s*\d{1,2}(\.\d+)?"\s*[EW]$', record.longitude):
                    raise ValidationError('Invalid longitude format. Use format: DD° MM\' SS.SSS" E/W')
    
    # Property Infrastructure Information
    road_width = fields.Char('Road Width')
    no_of_trees = fields.Char('No Of Trees')
    
    # Solar, Bore, Water, and Rainwater Information
    is_solar = fields.Char('Is Solar')
    no_of_solar = fields.Char('No Of Solar')
    is_bore = fields.Char('Is Boar')
    no_of_bore = fields.Char('No Of Boar')
    is_rainwater_harvesting = fields.Char('Is Rain water harvesting')
    no_of_rain_water_harvesting = fields.Char('No Of Rain Water harvesting')
    
    # Water Connection and Hand Pump Information
    is_water_conn_status = fields.Char('Is Warter Conn Status')
    is_hand_pump = fields.Char('Is Hand Pump')
    no_of_hand_pump = fields.Char('No Of Hand Pump')
    is_well = fields.Char('Is Well')
    no_of_well = fields.Char('No Of Well')
    
    # Lift, Drain, and Building Information
    is_lift = fields.Char('Is Lift')
    no_of_lift = fields.Char('No Of Lift')
    drain = fields.Char('Drain')
    building_permissions = fields.Char('Building Permissions')
    building_advertise = fields.Char('Building Advertise')
    building_advertise_type = fields.Char('Building Advertise Type')
    
    # Garbage Information
    garbage_segrigation = fields.Char('Garbage Segrigation')
    garbage_disposal = fields.Char('Garbage Disposal')
    septic_tank_yes_no = fields.Char('Septic Tank Yes/No')
    
    # Water Meter Information
    water_meter_yes_no = fields.Char('Water Meter Yes/No')
    water_connection_year = fields.Char('Water Connection Year')
    
    # License Information
    licence_no = fields.Char('Licence No')
    licence_date = fields.Date('Licence Date')
    
    # Property Construction Information
    year_of_permission = fields.Char('Year Of Permission')
    year_of_construction = fields.Char('Year Of Construction')
    building_age = fields.Char('Building Age')
    building_year = fields.Char('Building Year')
    build_completion_date = fields.Date('Build Completion Date')

    oid = fields.Date('Oid')
    
    # Fire, Water Meter, ETP, and Waste Information
    is_fire = fields.Char('Is Fire')
    no_of_fire = fields.Char('No Of Fire')
    water_meter_condition = fields.Char('Water Meter Condition')
    is_water_motar = fields.Char('Is Water Motar')
    water_connection_no = fields.Char('Water Connection No')
    water_consumer_no = fields.Char('Water Consumer No')
    is_etp = fields.Char('Is ETP')
    
    # Composting and Sewage Information
    is_home_composting = fields.Char('Is Home Composting')
    is_vermicompost = fields.Char('Is Vermi compost')
    is_echarging = fields.Char('Is ECharging')
    is_sewage_water = fields.Char('Is Sewage Water')
    
    # Permission and Certificate Information
    is_const_permission = fields.Char('Is Const Permission')
    const_completion_oc = fields.Char('Const Completion OC')
    gunthewari_certificate = fields.Char('Gunthewari Certificate')
    
    # Bukhand, Construction, and Animal Information
    is_bukhand = fields.Char('Is Bukhand')
    is_construction = fields.Char('Is Construction')
    total_no_of_people = fields.Char('Total No Of People')
    
    # Animal Information
    is_animals = fields.Char('Is Animals')
    dog = fields.Char('Dog')
    cat = fields.Char('Cat')
    cow = fields.Char('Cow')
    buffalo = fields.Char('Buffalo')
    horse = fields.Char('Horse')
    oax = fields.Char('Oax')
    pig = fields.Char('Pig')
    donkey = fields.Char('Donkey')
    other = fields.Char('Other')
    
    # Additional Information
    is_gotha = fields.Char('Is Gotha')
    oc_number = fields.Char('OC Number')

    microsite_url = fields.Char(string='Microsite URL', compute='_compute_microsite_url', store=False)

    @api.depends('uuid')
    def _compute_microsite_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for rec in self:
            if rec.uuid:
                rec.microsite_url = f"{base_url}/get/{rec.uuid}"
            else:
                rec.microsite_url = ''

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        """Override search_read to return decimal coordinates."""
        res = super().search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)
        
        if res and ('latitude' in (fields or []) or 'longitude' in (fields or [])):
            for record in res:
                # Use decimal coordinates for the map
                if 'latitude' in record:
                    record['latitude'] = str(record.get('latitude', ''))
                if 'longitude' in record:
                    record['longitude'] = str(record.get('longitude', ''))
                    
        return res

    currnet_tax = fields.Float('Current Tax')
    total_amount = fields.Float('Total Amount')
    