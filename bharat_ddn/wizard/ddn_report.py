from odoo import models, fields
from datetime import datetime

class DdnReport(models.TransientModel):
    _name = 'ddn.report'
    _description = 'DDN Report Wizard'

    date_from = fields.Date(string='Start Date', required=True)
    date_to = fields.Date(string='End Date', required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    zone_id = fields.Many2one('ddn.zone', string='Zone')
    ward_id = fields.Many2one('ddn.ward', string='Ward')



    def print_xlsx_report(self):
        data = {
            'form': self.read()[0]
        }
        return self.env.ref('bharat_ddn.action_report_property_survey_xlsx').report_action([], data=data)
    






class DdnPropertyXlsxReport(models.AbstractModel):
    _name = 'report.bharat_ddn.report_property_survey_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        form = data['form']
        zone_id = form.get('zone_id', False)
        ward_id = form.get('ward_id', False)
        date_from = form.get('date_from')
        date_to = form.get('date_to')
        company_id = form.get('company_id')

        domain = [('company_id', '=', company_id[0])]
        if zone_id:
            domain += [('zone_id', '=', zone_id[0])]
        if ward_id:
            domain += [('ward_id', '=', ward_id[0])]
        if date_from:
            domain += [('create_date', '>=', date_from)]
        if date_to:
            domain += [('create_date', '<=', date_to)]

        properties = self.env['ddn.property.info'].search(domain)

        worksheet = workbook.add_worksheet('Property Survey Report')
        bold = workbook.add_format({'bold': True})

        headers = [
            'Zone', 'Ward', 'Property ID', 'Unit', 'Address Line 1', 'Address Line 2',
            'Total Floors', 'Floor Number', 'Owner Name', 'Father Name', 'Area (Sq. Ft.)',
            'Area Code', 'Latitude', 'Longitude', 'Surveyor', 'Installer', 'Mobile No'
        ]
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, bold)

        row = 1
        for prop in properties:
            zone = prop.zone_id.name if prop.zone_id else ''
            ward = prop.ward_id.name if prop.ward_id else ''
            for survey in prop.survey_line_ids:
                worksheet.write(row, 0, zone)
                worksheet.write(row, 1, ward)
                worksheet.write(row, 2, survey.property_id.name or '')
                worksheet.write(row, 3, survey.unit or '')
                worksheet.write(row, 4, survey.address_line_1 or '')
                worksheet.write(row, 5, survey.address_line_2 or '')
                worksheet.write(row, 6, survey.total_floors or '')
                worksheet.write(row, 7, survey.floor_number or '')
                worksheet.write(row, 8, survey.owner_name or '')
                worksheet.write(row, 9, survey.father_name or '')
                worksheet.write(row, 10, survey.area or 0.0)
                worksheet.write(row, 11, survey.area_code or '')
                worksheet.write(row, 12, survey.latitude or '')
                worksheet.write(row, 13, survey.longitude or '')
                worksheet.write(row, 14, survey.surveyer_id.name or '')
                worksheet.write(row, 15, survey.installer_id.name or '')
                worksheet.write(row, 16, survey.mobile_no or '')
                row += 1
