from odoo import http
from .main import *
from odoo import http
from odoo.http import request, Response
from datetime import datetime, date, timedelta
import json
import logging
import logging
import boto3
import base64


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
            "property_type": property.property_type.name if property.property_type else '',
            "property_type_id": property.property_type.id if property.property_type else False,
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
            "is_solar": survey.is_solar,
            "is_rainwater_harvesting": survey.is_rainwater_harvesting,
        }

    @http.route('/api/property/create_survey', type='http', auth='public', methods=['POST'], csrf=False)
    @check_permission
    def create_survey(self, **kwargs):
        """Create a new survey for a property."""
        try:
            data = json.loads(request.httprequest.data or "{}")
            upic_no = data.get('upic_no', '')
            property_type_id = data.get('property_type_id')

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
            # Get company details for S3
            company_id = property_record.company_id
            if not company_id:
                return Response(json.dumps({'error': 'Company not found for the property'}), status=400, content_type='application/json')

            # Upload images to S3 if they exist
            property_image_url = None
            property_image1_url = None

            if data.get('property_image'):
                # Validate base64 string
                if not data['property_image'].strip():
                    return Response(json.dumps({'error': 'Empty property_image data'}), status=400, content_type='application/json')
                
                try:
                    property_image_url = self._upload_image_to_s3(
                        data['property_image'],
                        f"{upic_no}_1",
                        company_id
                    )
                except ValueError as ve:
                    return Response(json.dumps({'error': str(ve)}), status=400, content_type='application/json')
                except Exception as e:
                    _logger.error(f"Error uploading property_image: {str(e)}")
                    return Response(json.dumps({'error': f'Error uploading property_image: {str(e)}'}), status=500, content_type='application/json')

            if data.get('property_image1'):
                try:
                    property_image1_url = self._upload_image_to_s3(
                        data['property_image1'],
                        f"{upic_no}_2",
                        company_id
                    )
                except Exception as e:
                    _logger.error(f"Error uploading property_image1: {str(e)}")
                    return Response(json.dumps({'error': f'Error uploading property_image1: {str(e)}'}), status=500, content_type='application/json')
            
            # Add property_id to the data
            data['property_id'] = property_record.id
            data['image1_s3_url'] = property_image_url
            data['image2_s3_url'] = property_image1_url
            
            survey_line_vals = self._prepare_survey_line_vals(data)
            # Update both survey line and property status
            property_record.write({
                'survey_line_ids': [(0, 0, survey_line_vals)],
                'property_status': 'surveyed',
                'property_type': property_type_id
            })

            return Response(json.dumps({'message': 'Survey created successfully'}), status=200, content_type='application/json')

        except jwt.ExpiredSignatureError:
            _logger.error("JWT token has expired")
            raise AccessError('JWT token has expired')
        except jwt.InvalidTokenError:
            _logger.error("Invalid JWT token")
            raise AccessError('Invalid JWT token')
        except Exception as e:
            return Response(json.dumps({'error': str(e)}), status=500, content_type='application/json')

    def _upload_image_to_s3(self, image_data, s3_filename, company_id):
        """Upload image to S3 bucket and return the URL."""
        try:
            AWS_ACCESS_KEY = company_id.aws_acsess_key
            AWS_SECRET_KEY = company_id.aws_secret_key
            AWS_REGION = company_id.aws_region
            S3_BUCKET_NAME = company_id.s3_bucket_name

            if not all([AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, S3_BUCKET_NAME]):
                raise ValueError("Missing AWS credentials in company settings")

            s3_client = boto3.client(
                's3',
                aws_access_key_id=AWS_ACCESS_KEY,
                aws_secret_access_key=AWS_SECRET_KEY,
                region_name=AWS_REGION,
                verify=False  # ⚠️ Keep False only in dev
            )

            # ✅ Fix base64 padding
            def fix_base64_padding(b64_string):
                if not b64_string:
                    raise ValueError("Empty base64 string")
                missing_padding = len(b64_string) % 4
                if missing_padding:
                    b64_string += '=' * (4 - missing_padding)
                return b64_string


            fixed_b64 = fix_base64_padding(image_data)
            decoded_image = base64.b64decode(fixed_b64)


            s3_key = f"{s3_filename}.jpg"

            s3_client.put_object(
                Bucket=S3_BUCKET_NAME,
                Key=s3_key,
                Body=decoded_image,
                ContentType='image/jpeg'
            )


            return f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_key}"

        except Exception as e:
            _logger.error(f"Error in _upload_image_to_s3: {str(e)}")
            raise UserError(f"Failed to upload image to S3: {str(e)}")

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
            'is_solar': data.get("is_solar", True),  # Default to True if not provided
            'is_rainwater_harvesting': data.get("is_rainwater_harvesting", True),  # Default to True if not provided
        }

    @http.route('/api/create_property', type='http', auth='public', methods=['POST'], csrf=False)
    @check_permission
    def create_property_details(self, **kwargs):
        """Create a new property record."""
        try:
            data = json.loads(request.httprequest.data or "{}")
            
            # Validate required fields
            required_fields = ['company_id', 'surveyer_id', 'address_line_1', 'mobile']
            missing_fields = [field for field in required_fields if not data.get(field)]
            
            if missing_fields:
                return Response(
                    json.dumps({
                        'status': 'error',
                        'message': f'Missing required fields: {", ".join(missing_fields)}'
                    }),
                    status=400,
                    content_type='application/json'
                )

            vals = self._prepare_property_vals(data)
            property_record = request.env['ddn.property.info'].sudo().create(vals)
            
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

            # Get surveyor's ward
            surveyor = request.env['res.users'].sudo().browse(surveyor_id)
            if not surveyor:
                return Response(
                    json.dumps({'error': 'Surveyor not found'}),
                    status=404,
                    content_type='application/json'
                )
            
            ward_id = surveyor.ward_id.id if surveyor.ward_id else False

            if not ward_id:
                return Response(
                    json.dumps({'error': 'Surveyor does not have a ward assigned'}),
                    status=400,
                    content_type='application/json'
                )

            Property = request.env['ddn.property.info'].sudo()
            Survey = request.env['ddn.property.survey'].sudo()

            def get_counts(company_id, ward_id, surveyor_id):
                today = datetime.now().date()
                today_start = datetime.combine(today, datetime.min.time())
                today_end = datetime.combine(today, datetime.max.time())

                # Total properties in the ward (not filtered by surveyor)
                total = Property.search_count([
                    ('company_id', '=', company_id),
                    ('ward_id', '=', ward_id)
                ])

                # Today's surveyed count in the ward by this surveyor
                today_surveyed = Survey.search_count([
                    ('company_id', '=', company_id),
                    ('property_id.ward_id', '=', ward_id),
                    ('surveyer_id', '=', surveyor_id),
                    ('create_date', '>=', today_start),
                    ('create_date', '<=', today_end)
                ])

                # Today's discovered count
                today_discovered = Property.search_count([
                    ('company_id', '=', company_id),
                    ('ward_id', '=', ward_id),
                    ('property_status', '=', 'discovered'),
                    ('create_date', '>=', today_start),
                    ('create_date', '<=', today_end)
                ])

                # Calculate today's pending (total - today's surveyed - today's discovered)
                today_pending = total - today_surveyed - today_discovered

                # Overall counts (without date filter)
                surveyed = Survey.search_count([
                    ('company_id', '=', company_id),
                    ('property_id.ward_id', '=', ward_id),
                    ('surveyer_id', '=', surveyor_id)
                ])

                discovered = Property.search_count([
                    ('company_id', '=', company_id),
                    ('ward_id', '=', ward_id),
                    ('property_status', '=', 'discovered')
                ])

                pending = total - surveyed - discovered

                return {
                    'total': total,
                    'today_surveyed': today_surveyed,
                    'today_discovered': today_discovered,
                    'today_pending': today_pending,
                    'surveyed': surveyed,
                    'discovered': discovered,
                    'pending': pending,
                }

            counts = get_counts(company_id, ward_id, surveyor_id)

            def percent(val):
                # Dummy logic, replace with real calculation if available
                return round(5 + 20 * (0.5 - (val % 2)), 1)

            response = {
                "status": "success",
                "message": "Dashboard data fetched successfully",
                "today": [
                    {
                        "label": "Total Properties",
                        "value": counts['total'],
                        "percent": f"+{percent(counts['total'])}%",
                    },
                    {
                        "label": "Today's Surveyed",
                        "value": counts['today_surveyed'],
                        "percent": f"+{percent(counts['today_surveyed'])}%",
                    },
                    {
                        "label": "Today's Discovered",
                        "value": counts['today_discovered'],
                        "percent": f"+{percent(counts['today_discovered'])}%",
                    },
                    {
                        "label": "Today's Pending",
                        "value": counts['today_pending'],
                        "percent": f"{percent(counts['today_pending'])}%",
                    },
                ],
                "overall": [
                    {
                        "label": "Total Properties",
                        "value": counts['total'],
                        "percent": f"+{percent(counts['total'])}%",
                    },
                    {
                        "label": "Surveyed",
                        "value": counts['surveyed'],
                        "percent": f"+{percent(counts['surveyed'])}%",
                    },
                    {
                        "label": "Discovered",
                        "value": counts['discovered'],
                        "percent": f"+{percent(counts['discovered'])}%",
                    },
                    {
                        "label": "Pending",
                        "value": counts['pending'],
                        "percent": f"{percent(counts['pending'])}%",
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
        # Get zone and ward IDs from names if provided
        zone_id = False
        ward_id = False
        
        if data.get('zone_name'):
            zone = request.env['ddn.zone'].sudo().search([('name', '=', data['zone_name'])], limit=1)
            zone_id = zone.id if zone else False
        
        if data.get('ward_name'):
            ward = request.env['ddn.ward'].sudo().search([('name', '=', data['ward_name'])], limit=1)
            ward_id = ward.id if ward else False

        # Get colony ID if colony_name is provided
        colony_id = False
        if data.get('colony_name'):
            colony = request.env['ddn.colony'].sudo().search([('name', '=', data['colony_name'])], limit=1)
            colony_id = colony.id if colony else False

        return {
            'company_id': data.get('company_id'),
            'address_line_1': data.get('address_line_1'),
            'address_line_2': data.get('address_line_2'),
            'mobile_no': data.get('mobile'),
            'owner_name': data.get('owner_name'),
            'longitude': data.get('longitude'),
            'latitude': data.get('latitude'),
            'surveyer_id': data.get('surveyer_id'),
            'zone_id': zone_id or data.get('zone_id'),
            'ward_id': ward_id or data.get('ward_id'),
            'colony_id': colony_id,
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

            # Get unique properties from the surveys
            properties = recent_surveys.mapped('property_id')
            
            # Format the response using the same format as get_property
            property_data = [self._format_property_data(property) for property in properties]

            return Response(
                json.dumps({
                    'property_details': property_data,
                    'matched_count': len(property_data),
                    'message': 'Recent surveys fetched successfully'
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

    @http.route('/api/surveyor/surveys', type='http', auth='public', methods=['GET'], csrf=False)
    @check_permission
    def list_surveyor_surveys(self, **kwargs):
        try:
            page = int(request.httprequest.args.get('page', 1))
            limit = int(request.httprequest.args.get('limit', 10))
            offset = (page - 1) * limit

            # Use the new helper function
            user_id = extract_user_id_from_token(request.httprequest.headers.get('Authorization'))
            if not user_id:
                return Response(
                    json.dumps({'error': 'Invalid or missing authorization token'}),
                    status=401,
                    content_type='application/json'
                )

            # Search for properties surveyed by this surveyor
            domain = [('surveyer_id', '=', user_id)]
            
            # Get total count for pagination
            total_count = request.env['ddn.property.info'].sudo().search_count(domain)
            
            # Get paginated records
            properties = request.env['ddn.property.info'].sudo().search(
                domain,
                offset=offset,
                limit=limit,
                order='id desc'
            )

            # Format the response data
            survey_list = []
            for property in properties:
                survey_data = {
                    'upic_no': property.upic_no,
                    'property_id': property.id,
                    'status': property.property_status,
                    'address': {
                        'line1': property.address_line_1,
                        'line2': property.address_line_2
                    },
                    'owner_name': property.owner_name,
                    'mobile_no': property.mobile_no,
                    'zone': property.zone_id.name if property.zone_id else '',
                    'ward': property.ward_id.name if property.ward_id else '',
                    'colony': property.colony_id.name if property.colony_id else '',
                    'property_type': property.property_type.name if property.property_type else '',
                    'survey_details': []
                }

                # Add survey details if available
                for survey in property.survey_line_ids:
                    survey_details = {
                        'area': survey.area,
                        'total_floors': survey.total_floors,
                        'floor_number': survey.floor_number,
                        'father_name': survey.father_name,
                        'survey_date': survey.create_date.strftime('%Y-%m-%d %H:%M:%S') if survey.create_date else '',
                        'images': {
                            'image1': survey.image1_s3_url,
                            'image2': survey.image2_s3_url
                        }
                    }
                    survey_data['survey_details'].append(survey_details)

                survey_list.append(survey_data)

            response = {
                'status': 'success',
                'data': {
                    'surveys': survey_list,
                    'pagination': {
                        'total_records': total_count,
                        'total_pages': (total_count + limit - 1) // limit,
                        'current_page': page,
                        'limit': limit
                    }
                }
            }

            return Response(
                json.dumps(response),
                status=200,
                content_type='application/json'
            )

        except Exception as e:
            return Response(
                json.dumps({
                    'status': 'error',
                    'message': 'An error occurred',
                    'details': str(e)
                }),
                status=500,
                content_type='application/json'
            )

def extract_user_id_from_token(token):
    if not token:
        raise AccessError('Authorization header is missing or invalid')
    if token.startswith("Bearer "):
        token = token[7:]
    decoded_token = jwt.decode(token, options={"verify_signature": False})
    return decoded_token['user_id']


