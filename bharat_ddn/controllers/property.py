from odoo import http
from .main import *
from odoo import http
from odoo.http import request, Response
from datetime import datetime, date, timedelta
import json
import logging


_logger = logging.getLogger(__name__)
from datetime import datetime

# Constants
DEFAULT_LIMIT = 50
DEFAULT_PAGE = 1
PROPERTY_STATUSES = ['uploaded', 'pdf_downloaded', 'surveyed', 'discovered']

class PropertyDetailsAPI(http.Controller):
    """API controller for property details."""

    """ API CRUD """
        
    @http.route('/api/get_property', type='http', auth='public', methods=['POST'], csrf=False)
    @check_permission
    def get_property_details(self, **kwargs):
        """Get property details based on a single parameter (UPIC, mobile number, or UUID)."""
        try:
            data = json.loads(request.httprequest.data or "{}")
            parameter = data.get('parameter_name', '').strip()
            page = int(data.get('page', DEFAULT_PAGE))
            limit = int(data.get('limit', DEFAULT_LIMIT))

            domain = []
            if parameter:
                if parameter.isdigit() and len(parameter) == 10:
                    domain.append(('mobile_no', '=', parameter))
                elif len(parameter) == 36:  # UUID length is 36 characters
                    domain.append(('uuid', '=', parameter))
                else:
                    domain.append(('upic_no', '=', parameter))

            _logger.info(f"Searching with domain: {domain} and parameter: {parameter}")

            if domain:
                property_details = request.env['ddn.property.info'].sudo().search(domain, limit=1)
            else:
                property_details = []  # Explicitly return empty if no valid input

            property_data = [self._format_property_data(property) for property in property_details]

            return Response(json.dumps({
                'property_details': property_data,
                'matched_count': len(property_data),
                'page': page,
                'limit': limit,
                'message': 'No property found for the given parameter.' if not property_data else 'Property found.'
            }), status=200, content_type='application/json')

        except jwt.ExpiredSignatureError:
            raise AccessError('JWT token has expired')
        except jwt.InvalidTokenError:
            raise AccessError('Invalid JWT token')

    def _format_property_data(self, property):
        """Format property data for response."""
        return {
            "status": property.property_status,
            "upic_no": property.upic_no,
            "zone_id": property.zone_id.name,
            "ward_id": property.ward_id.name,
            "colony_name": property.colony_id.name if property.colony_id else '',
            "unit_no": property.unit_no if property.unit_no else '',
            "latitude": property.latitude,
            "longitude": property.longitude,
            "mobile_no": property.mobile_no,
            "owner_name": property.owner_name,
            "survey_line_ids": [self._format_survey_data(survey) for survey in property.survey_line_ids if property.survey_line_ids]
        }

    def _format_survey_data(self, survey):
        """Format survey data for response."""
        return {
            "address_line_1": survey.address_line_1,
            "address_line_2": survey.address_line_2,
            "mobile_no": survey.mobile_no,
            "unit": survey.unit,
            "total_floors": survey.total_floors,
            "floor_number": survey.floor_number,
            "owner_name": survey.owner_name,
            "father_name": survey.father_name,
            "area": survey.area,
            "area_code": survey.area_code,
            "longitude": survey.longitude,
            "latitude": survey.latitude,
            "surveyer_id": survey.surveyer_id.id,
            "installer_id": survey.installer_id.id,
            "property_image": str(survey.property_image),
            "property_image1": str(survey.property_image1),
        }

    @http.route('/api/property/create_survey', type='http', auth='public', methods=['POST'], csrf=False)
    @check_permission
    def create_survey(self, **kwargs):
        """Create a new survey for a property."""
        _logger.info("create_survey API endpoint hit")

        try:
            data = json.loads(request.httprequest.data or "{}")
            upic_no = data.get('upic_no', '')
            if not upic_no:
                return Response(json.dumps({'error': 'upic_no is required'}), status=400, content_type='application/json')
            
            property_record = request.env['ddn.property.info'].sudo().search([('upic_no', '=', upic_no)])

            if not property_record:
                return Response(json.dumps({'error': 'Property not found for the provided upic_no'}), status=404, content_type='application/json')
            
            # Check if property status is pdf_downloaded
            if property_record.property_status != 'pdf_downloaded':
                return Response(
                    json.dumps({
                        'error': 'Survey can only be created for properties with status "pdf_downloaded"'
                    }), 
                    status=400, 
                    content_type='application/json'
                )
            
            survey_line_vals = self._prepare_survey_line_vals(data)

            # Update both survey line and property status
            property_record.write({
                'survey_line_ids': [(0, 0, survey_line_vals)],
                'property_status': 'surveyed'  # Update property status to surveyed
            })

            _logger.info(f"Successfully created a new survey for property {upic_no}")
            return Response(json.dumps({'message': 'Survey created successfully'}), status=200, content_type='application/json')

        except jwt.ExpiredSignatureError:
            _logger.error("JWT token has expired")
            raise AccessError('JWT token has expired')
        except jwt.InvalidTokenError:
            _logger.error("Invalid JWT token")
            raise AccessError('Invalid JWT token')
        except Exception as e:
            _logger.error(f"Error occurred: {str(e)}")
            return Response(json.dumps({'error': str(e)}), status=500, content_type='application/json')

    def _prepare_survey_line_vals(self, data):
        """Prepare survey line values from data."""
        return {
            'company_id': data.get("company_id"),
            'property_id': data.get("property_id", False),
            'address_line_1': data.get("address_line_1", ''),
            'address_line_2': data.get("address_line_2", ''),
            'unit': data.get("unit", ''),
            'total_floors': data.get("total_floors", ''),
            'mobile_no': data.get("mobile_no", False),
            'floor_number': data.get("floor_number", ''),
            'owner_name': data.get("owner_name", ''),
            'father_name': data.get("father_name", ''),
            'longitude': data.get("longitude", ''),
            'latitude': data.get("latitude", ''),
            'surveyer_id': data.get("surveyer_id", False),
            'property_image': data.get("property_image", False),
            'property_image1': data.get("property_image1", False),
        }

    @http.route('/api/create_property', type='http', auth='public', methods=['POST'], csrf=False)
    @check_permission
    def create_property_details(self, **kwargs):
        """Create a new property record."""
        try:
            data = json.loads(request.httprequest.data or "{}")
            vals = self._prepare_property_vals(data)
            property_record = request.env['ddn.property.info'].sudo().create(vals)
            property_record.property_status = 'discovered'  # Update property status to surveyed
            
            return Response(
                json.dumps({
                    'status': 'success',
                    'message': 'Property created successfully',
                    'property_id': property_record.id
                }),
                status=200,
                content_type='application/json'
            )

        except jwt.ExpiredSignatureError:
            _logger.error("JWT token has expired")
            return Response(
                json.dumps({'status': 'error', 'message': 'JWT token has expired'}),
                status=401,
                content_type='application/json'
            )

        except jwt.InvalidTokenError:
            _logger.error("Invalid JWT token")
            return Response(
                json.dumps({'status': 'error', 'message': 'Invalid JWT token'}),
                status=401,
                content_type='application/json'
            )

        except Exception as e:
            _logger.error(f"Error occurred: {str(e)}")
            return Response(
                json.dumps({'status': 'error', 'message': 'An error occurred', 'details': str(e)}),
                status=500,
                content_type='application/json'
            )
        

    @http.route(['/api/dashboard'], type='http', auth='public', methods=['POST'], csrf=False)
    def dashboard_summary(self, **kwargs):
        """Get dashboard summary data."""
        try:
            data = json.loads(request.httprequest.data or "{}")
            Property = request.env['ddn.property.info'].sudo()

            surveyor_id = data.get('surveyor_id')
            company_id = data.get('company_id')

            today_from = datetime.combine(date.today(), datetime.min.time())
            today_to = datetime.combine(date.today() + timedelta(days=1), datetime.min.time())

            today_domain = [('company_id', '=', company_id), ('surveyer_id', '=', surveyor_id),
                            ('create_date', '>=', today_from), ('create_date', '<', today_to)]

            today_data = self._get_status_counts(Property, today_domain)

            if data.get('date_from') and data.get('date_to'):
                date_from = datetime.strptime(data['date_from'], "%Y/%m/%d")
                date_to = datetime.strptime(data['date_to'], "%Y/%m/%d")
            else:
                date_from = datetime.min
                date_to = datetime.now()

            all_domain = [('company_id', '=', company_id), ('surveyer_id', '=', surveyor_id),
                          ('create_date', '>=', date_from), ('create_date', '<', date_to)]

            all_data = self._get_status_counts(Property, all_domain)

            return Response(
                json.dumps({
                    'status': 'success',
                    'message': 'Dashboard data fetched successfully',
                    'today': today_data,
                    'all': all_data
                }),
                status=200,
                content_type='application/json'
            )

        except Exception as e:
            return Response(
                json.dumps({'status': 'error', 'message': 'An error occurred', 'details': str(e)}),
                status=500,
                content_type='application/json'
            )

    def _get_status_counts(self, Property, domain):
        """Get counts for each property status."""
        return {status: Property.search_count(domain + [('property_status', '=', status)]) for status in PROPERTY_STATUSES}

    def _prepare_property_vals(self, data):
        """Prepare property values from data."""
        return {
            'company_id': data.get('company_id'),
            'address_line_1': data.get('address_line_1'),
            'address_line_2': data.get('address_line_2'),
            'mobile_no': data.get('mobile'),
            'owner_name': data.get('owner_name'),
            'longitude': data.get('longitude'),
            'latitude': data.get('latitude'),
            'surveyer_id': data.get('surveyer_id'),
            'zone_id': data.get('zone_id'),
            'ward_id': data.get('ward_id'),
            'property_status': 'discovered'
        }

    @http.route('/api/recent_surveys', type='http', auth='public', methods=['POST'], csrf=False)
    @check_permission
    def get_recent_surveys(self, **kwargs):
        """Get top 5 most recent surveys based on surveyor ID and (optionally) ward ID."""
        try:
            data = json.loads(request.httprequest.data or "{}")
            surveyor_id = data.get('surveyor_id')
            ward_id = data.get('ward_id')

            if not surveyor_id:
                return Response(
                    json.dumps({'error': 'surveyor_id is required'}),
                    status=400,
                    content_type='application/json'
                )

            # Build domain
            domain = [('surveyer_id', '=', surveyor_id)]
            if ward_id:
                domain.append(('property_id.ward_id', '=', ward_id))

            # Get the top 5 most recent surveys
            recent_surveys = request.env['ddn.property.survey'].sudo().search(
                domain,
                order='create_date desc',
                limit=5
            )

            survey_data_list = []
            for survey in recent_surveys:
                survey_data = {
                    'upic_no': survey.property_id.upic_no,
                    'ward_name': survey.property_id.ward_id.name,
                    'zone_name': survey.property_id.zone_id.name,
                    'owner_name': survey.owner_name,
                    'mobile_no': survey.mobile_no,
                    'address': f"{survey.address_line_1}, {survey.address_line_2}",
                    'created_date': survey.create_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'property_image': str(survey.property_image),
                    'property_image1': str(survey.property_image1),
                    'total_floors': survey.total_floors,
                    'floor_number': survey.floor_number,
                    'unit': survey.unit
                }
                survey_data_list.append(survey_data)

            return Response(
                json.dumps({
                    'status': 'success',
                    'message': 'Recent surveys fetched successfully',
                    'recent_surveys': survey_data_list
                }),
                status=200,
                content_type='application/json'
            )

        except Exception as e:
            _logger.error(f"Error in get_recent_surveys: {str(e)}")
            return Response(
                json.dumps({'error': str(e)}),
                status=500,
                content_type='application/json'
            )

class PropertyIdDataAPI(http.Controller):
    @http.route('/api/property_id_data/search', type='http', auth='public', methods=['POST'], csrf=False)
    def search_property_id_data(self, **kwargs):
        try:
            data = json.loads(request.httprequest.data or '{}')
            parameter = data.get('parameter_name', '').strip()
            
            if not parameter:
                return Response(json.dumps({'error': 'Please provide parameter_name'}), status=400, content_type='application/json')
            
            # Search across all relevant fields
            records = request.env['property.id.data'].sudo().search([
                '|',  # OR condition
                '|',  # OR condition
                ('mobile_no', '=', parameter),
                ('property_id', '=', parameter),
                ('owner_name', 'ilike', parameter)
            ])
            
            result = [
                {
                    'property_id': rec.property_id,
                    'owner_name': rec.owner_name,
                    'address': rec.address,
                    'mobile_no': rec.mobile_no,
                    'currnet_tax': rec.currnet_tax,
                    'total_amount': rec.total_amount,
                }
                for rec in records
            ]
            return Response(json.dumps({'results': result}), status=200, content_type='application/json')
        except Exception as e:
            return Response(json.dumps({'error': str(e)}), status=500, content_type='application/json')


