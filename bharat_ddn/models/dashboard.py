from odoo import models, fields, api
import itertools


class PropertyInfo(models.Model):
    _inherit = 'ddn.property.info'


    @api.model
    def get_dashboard_data(self):
        PropertyInfo = self.env['ddn.property.info'].search([])
        sorted_records = sorted(PropertyInfo, key=lambda rec: rec.ward_no.name if rec.ward_no else '')
        grouped_records = itertools.groupby(sorted_records, key=lambda rec: rec.ward_no.name if rec.ward_no else '') 
        result = {}

        for group_key, grp in grouped_records:
            count = 0
            new = 0
            uploaded = 0
            pdf_downloaded = 0
            surveyed = 0
            unlocked = 0
            discovered = 0
            ward_zone_name = None  # Add zone

            for rec in grp:
                count += 1
                if rec.property_status == 'new':
                    new += 1
                if rec.property_status == 'uploaded':
                    uploaded += 1
                if rec.property_status == 'pdf_downloaded':
                    pdf_downloaded += 1
                if rec.property_status == 'surveyed':
                    surveyed += 1
                if rec.property_status == 'unlocked':
                    unlocked += 1
                if rec.property_status == 'discovered':
                    discovered += 1

                if not ward_zone_name and rec.ward_no and rec.ward_no.zone_id:
                    ward_zone_name = rec.ward_no.zone_id.name

            result[group_key] = {
                'count': count,
                'new': new,
                'uploaded': uploaded,
                'pdf_downloaded': pdf_downloaded,
                'surveyed': surveyed,
                'unlocked': unlocked,
                'discovered': discovered,
                'zone': ward_zone_name  # Include zone in result
            }

        final_result = [{
            'total_count': self.env['ddn.property.info'].search_count([]),
            'total_uploaded': self.env['ddn.property.info'].search_count([('property_status', '=', 'uploaded')]),
            'total_pdf_downloaded': self.search_count([('property_status', '=', 'pdf_downloaded')]),
            'total_surveyed': self.search_count([('property_status', '=', 'surveyed')]),
            'total_unlocked': self.search_count([('property_status', '=', 'unlocked')]),
            'total_discovered': self.search_count([('property_status', '=', 'discovered')]),
            'total_zones': self.env['ddn.zone'].search_count([]),
            'total_wards': self.env['ddn.ward'].search_count([]),
            'total_users': self.env['res.users'].search_count([]),
            'ward_data': [
                {
                    'ward': ward,
                    'zone': data.get('zone'),
                    'total_count': data['count'],
                    'uploaded_count': data['uploaded'],
                    'pdf_downloaded_count': data['pdf_downloaded'],
                    'surveyed_count': data['surveyed'],
                    'unlocked_count': data['unlocked'],
                    'discovered_count': data['discovered'],
                } for ward, data in result.items()
            ]
        }]

        print("result - ", final_result)
        return final_result
