from odoo import models, fields
from datetime import datetime

class DdnReport(models.TransientModel):
    _name = 'ddn.report'
    _description = 'DDN Report Wizard'

    date_from = fields.Date(string='Start Date', required=True)
    date_to = fields.Date(string='End Date', required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    zone_id = fields.Many2many('ddn.zone', string='Zone')
    ward_id = fields.Many2many('ddn.ward', string='Ward')



    def print_xlsx_report(self):
        print("funtion is working fine")
        data = {
            'form': self.read()[0]
        }
        return self.env.ref('bharat_ddn.action_report_property_survey_xlsx').report_action([], data=data)
    

class PropertySurveyXlsxReport(models.AbstractModel):
    _name = 'report.bharat_ddn.report_property_survey_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Survey XLSX Report'

    def generate_xlsx_report(self, workbook, data, wizard):
        sheet = workbook.add_worksheet("Survey Report")
        # Style
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
        text_format = workbook.add_format({'border': 1})
        text_format1 = workbook.add_format({'border': 1, "bold":True,'font_size': 25, 'align': 'left', 'valign': 'vcenter','bg_color': '#D3D3D3'})

        datetime_format = workbook.add_format({
            'num_format': 'dd-mm-yyyy hh:mm:ss',
            'align': 'left',
            'border': 1
        })

        datetime_format1 = workbook.add_format({
            'num_format': 'dd-mm-yyyy',
            'align': 'left',
            'border': 1
        })

        sheet.set_column('A:B', 15)
        sheet.set_column('C:D', 8)
        sheet.set_column('E:J', 18)
        sheet.set_column('O:Q', 18)
        sheet.set_column('R:R', 60)

        sheet.set_row(1, 30)
        sheet.merge_range("A2:R2", "Survey Report", text_format1)
        sheet.write(3,0, "Date From", text_format)
        sheet.write(3,1, wizard.date_from, datetime_format1)
        sheet.write(4,0, "Date To", text_format)
        sheet.write(4,1, wizard.date_to, datetime_format1)

        headers = [
            "UPIC No", 
            "Property Id", 
            "Zone", 
            "Ward", 
            "Colony",
            "Owner Name", 
            "Father Name", 
            "Mobile No", 
            "Address Line 1", 
            "Address Line 2",
            "Latitude", 
            "Longitude",
            "Total Floors", 
            "Floor Number", 
            "Surveyor",
            "Surveyor Datetime",
            "Property Type",
            "Microsite Url",
        ]

        for col, header in enumerate(headers):
            sheet.write(6, col, header, header_format)

        # Get data
        domain = [('company_id', '=', wizard.company_id.id)]

        if wizard.zone_id:
            domain += [('property_id.zone_id', 'in', wizard.zone_id.ids)]
        if wizard.ward_id:
            domain += [('property_id.ward_id', 'in', wizard.ward_id.ids)]
        if wizard.date_from:
            domain += [('create_date', '>=', wizard.date_from)]
        if wizard.date_to:
            domain += [('create_date', '<=', wizard.date_to)]

        survey_records = self.env['ddn.property.survey'].search(domain)

        row = 7
        for rec in survey_records:
            prop = rec.property_id

            sheet.write(row, 0, prop.upic_no or '', text_format)
            sheet.write(row, 1, prop.property_no or '', text_format)
            sheet.write(row, 2, prop.zone_id.name or '', text_format)
            sheet.write(row, 3, prop.ward_id.name or '', text_format)
            sheet.write(row, 4, prop.colony_id.name or '', text_format)
            sheet.write(row, 5, rec.owner_name or '', text_format)
            sheet.write(row, 6, rec.father_name or '', text_format)
            sheet.write(row, 7, rec.mobile_no or '', text_format)
            sheet.write(row, 8, rec.address_line_1 or '', text_format)
            sheet.write(row, 9, rec.address_line_2 or '', text_format)
            sheet.write(row, 10, rec.latitude or '', text_format)
            sheet.write(row, 11, rec.longitude or '', text_format)
            sheet.write(row, 12, rec.total_floors or '', text_format)
            sheet.write(row, 13, rec.floor_number or '', text_format)
            sheet.write(row, 14, rec.surveyer_id.name or '', text_format)
            sheet.write(row, 15, rec.create_date or '', datetime_format)
            sheet.write(row, 16, rec.property_id.property_type.name or '', text_format)
            sheet.write(row, 17, rec.property_id.microsite_url or '', text_format)
            row += 1
