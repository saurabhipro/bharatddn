from odoo import http
from .main import *
from odoo import http
from odoo.http import request, Response
from datetime import datetime, date, timedelta
import json
import logging
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
            "property_type": property.property_type_id.name if property.property_type_id else '',
            "property_type_id": property.property_type_id.id if property.property_type_id else False,
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
            property_type_id = data.get('property_type_id')  # Get property_type_id from request

            if not upic_no:
                return Response(json.dumps({'error': 'upic_no is required'}), status=400, content_type='application/json')
            
            if not property_type_id:
                return Response(json.dumps({'error': 'property_type_id is required'}), status=400, content_type='application/json')
            
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
            
            # Add property_id to the data
            data['property_id'] = property_record.id
            survey_line_vals = self._prepare_survey_line_vals(data)

            # Update both survey line and property status
            property_record.write({
                'survey_line_ids': [(0, 0, survey_line_vals)],
                'property_status': 'surveyed',  # Update property status to surveyed
                'property_type': property_type_id  # Update property type in the property record
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
        

    @http.route('/api/dashboard', type='http', auth='public', methods=['POST'], csrf=False)
    @check_permission
    def dashboard_summary(self, **kwargs):
        """Get dashboard summary data for today's progress and overall summary."""
        try:
            data = json.loads(request.httprequest.data or "{}")
            surveyor_id = data.get('surveyor_id')
            company_id = data.get('company_id')
            ward_id = data.get('ward_id')  # NEW: get ward_id

            today_from = datetime.combine(date.today(), datetime.min.time())
            today_to = datetime.combine(date.today() + timedelta(days=1), datetime.min.time())

            Property = request.env['ddn.property.info'].sudo()

            def get_counts(domain):
                return {
                    'total': Property.search_count(domain),
                    'surveyed': Property.search_count(domain + [('property_status', '=', 'surveyed')]),
                    'discovered': Property.search_count(domain + [('property_status', '=', 'discovered')]),
                    'pending': Property.search_count(domain + [('property_status', '=', 'pending')]),
                }

            # Build domains with optional ward_id
            today_domain = [
                ('company_id', '=', company_id),
                ('surveyer_id', '=', surveyor_id),
                ('create_date', '>=', today_from),
                ('create_date', '<', today_to)
            ]
            all_domain = [
                ('company_id', '=', company_id),
                ('surveyer_id', '=', surveyor_id)
            ]
            if ward_id:
                today_domain.append(('ward_id', '=', ward_id))
                all_domain.append(('ward_id', '=', ward_id))

            today_counts = get_counts(today_domain)
            all_counts = get_counts(all_domain)

            def percent(val):
                # Dummy logic, replace with real calculation if available
                return round(5 + 20 * (0.5 - (val % 2)), 1)

            response = {
                "status": "success",
                "message": "Dashboard data fetched successfully",
                "today": [
                    {
                        "label": "Total Properties",
                        "value": today_counts['total'],
                        "percent": f"+{percent(today_counts['total'])}%",
                    },
                    {
                        "label": "Surveyed",
                        "value": today_counts['surveyed'],
                        "percent": f"+{percent(today_counts['surveyed'])}%",
                    },
                    {
                        "label": "Discovered",
                        "value": today_counts['discovered'],
                        "percent": f"+{percent(today_counts['discovered'])}%",
                    },
                    {
                        "label": "Pending",
                        "value": today_counts['pending'],
                        "percent": f"{percent(today_counts['pending'])}%",
                    },
                ],
                "overall": [
                    {
                        "label": "Total Properties",
                        "value": all_counts['total'],
                        "percent": f"+{percent(all_counts['total'])}%",
                    },
                    {
                        "label": "Surveyed",
                        "value": all_counts['surveyed'],
                        "percent": f"+{percent(all_counts['surveyed'])}%",
                    },
                    {
                        "label": "Discovered",
                        "value": all_counts['discovered'],
                        "percent": f"+{percent(all_counts['discovered'])}%",
                    },
                    {
                        "label": "Pending",
                        "value": all_counts['pending'],
                        "percent": f"{percent(all_counts['pending'])}%",
                    },
                ]
            }
            return Response(json.dumps(response), status=200, content_type='application/json')

        except Exception as e:
            return Response(
                json.dumps({'status': 'error', 'message': 'An error occurred', 'details': str(e)}),
                status=500,
                content_type='application/json'
            )

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
            'property_status': 'discovered',
            'property_type_id': data.get('property_type_id'),
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

    @http.route('/api/property_types', type='http', auth='public', methods=['GET'], csrf=False)
    @check_permission
    def get_property_types(self, **kwargs):
        """Get all property types with their names and IDs."""
        try:
            property_types = request.env['ddn.property.type'].sudo().search([])
            
            property_type_list = [{
                'id': pt.id,
                'name': pt.name,
                'code': pt.code if hasattr(pt, 'code') else '',
                'description': pt.description if hasattr(pt, 'description') else '',
                'group_id': pt.group_id.id if pt.group_id else False,
                'group_name': pt.group_id.name if pt.group_id else ''
            } for pt in property_types]

            return Response(
                json.dumps({
                    'status': 'success',
                    'message': 'Property types fetched successfully',
                    'property_types': property_type_list
                }),
                status=200,
                content_type='application/json'
            )

        except Exception as e:
            _logger.error(f"Error in get_property_types: {str(e)}")
            return Response(
                json.dumps({
                    'status': 'error',
                    'message': 'An error occurred while fetching property types',
                    'details': str(e)
                }),
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


