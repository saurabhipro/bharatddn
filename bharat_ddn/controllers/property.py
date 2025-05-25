from odoo import http
from .main import *

from odoo import http
from odoo.http import request, Response
from datetime import datetime, date, timedelta
import json


_logger = logging.getLogger(__name__)
from datetime import datetime
class PropertyDetailsAPI(http.Controller):

    """ API CRUD """
        
    @http.route('/api/get_property', type='http', auth='public', methods=['POST'], csrf=False)
    @check_permission
    def get_property_details(self, **kwargs):
        try:
            data = json.loads(request.httprequest.data or "{}")

            name = data.get('name')
            page = int(data.get('page', 1))
            limit = int(data.get('limit', 50))

            domain = []
            if name:
                if 'ddn' in name.lower() and not name.isdigit():
                    domain.append(('upic_no', '=', name))
                elif name.isdigit():
                    domain.append(('mobile_no', '=', name))
                else:
                    domain.append(('owner_name', 'like', name))


            if domain:
                property_details = request.env['ddn.property.info'].sudo().search(domain, limit=limit, offset=(page - 1) * limit)
            else:
                property_details = request.env['ddn.property.info'].sudo().search([], limit=limit, offset=(page - 1) * limit)

            property_data = []
            for property in property_details:
                property_data.append({
                    "status" : property.property_status,
                    "owner_id": property.owner_id,
                    "upic_no": property.upic_no,
                    "zone_no": property.zone_no.name,
                    "ward_no": property.ward_no.name,
                    "latitude": property.latitude,
                    "longitude": property.longitude,
                    "mobile_no": property.mobile_no,
                    "owner_name": property.owner_name,
                    "occupier_name": property.occupier_name,
                    "owner_dukan_imarate_nav": property.owner_dukan_imarate_nav,
                    "plot_area": property.plot_area,
                    "renter_name": property.renter_name,
                    "survey_line_ids": [{
                                        "address_line_1": survey.address_line_1, 
                                        "address_line_2": survey.address_line_2, 
                                        "colony_name": survey.colony_name, 
                                        "street": survey.street, 
                                        "mobile_no":survey.mobile_no,
                                        "house_number": survey.house_number, 
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
                                    } for survey in property.survey_line_ids if property.survey_line_ids]
                })

            # Return the paginated response
            return Response(json.dumps({
                'property_details': property_data,
                'page': page,
                'limit': limit
            }), status=200, content_type='application/json')

        except jwt.ExpiredSignatureError:
            raise AccessError('JWT token has expired')
        except jwt.InvalidTokenError:
            raise AccessError('Invalid JWT token')

    @http.route('/api/property/create_survey', type='http', auth='public', methods=['POST'], csrf=False)
    @check_permission
    def create_survey(self, **kwargs):
        _logger.info("create_survey API endpoint hit")

        try:
            data = json.loads(request.httprequest.data or "{}")
            upic_no = data.get('upic_no', '')
            if not upic_no:
                return Response(json.dumps({'error': 'upic_no is required'}), status=400, content_type='application/json')
            
            property_record = request.env['ddn.property.info'].sudo().search([('upic_no', '=', upic_no)])

            if not property_record:
                return Response(json.dumps({'error': 'Property not found for the provided upic_no'}), status=404, content_type='application/json')
            
            address_line_1 = data.get("address_line_1", '')
            address_line_2 = data.get("address_line_2", '')
            colony_name = data.get("colony_name", '')
            street = data.get("street", '')
            house_number = data.get("house_number", '')
            unit = data.get("unit", '')
            total_floors = data.get("total_floors", '')
            mobile_no = data.get("mobile_no", False)
            floor_number = data.get("floor_number", '')
            owner_name = data.get("owner_name", '')
            father_name = data.get("father_name", '')
            area = data.get("area", '')
            area_code = data.get("area_code", '')
            longitude = data.get("longitude", '')
            latitude = data.get("latitude", '')
            surveyer_id = data.get("surveyer_id", False)
            installer_id = data.get("installer_id", False)
            company_id = data.get("company_id")
            property_image = data.get("property_image", False)
            property_image1 = data.get("property_image1", False)


            if surveyer_id:
                surveyer_user = request.env['res.users'].sudo().browse(surveyer_id)
                if not surveyer_user.exists():
                    return Response(json.dumps({'error': f"Surveyor with ID {surveyer_id} does not exist"}), status=400, content_type='application/json')

            # Prepare the survey line values
            survey_line_vals = {
                'address_line_1': address_line_1,
                'address_line_2': address_line_2,
                'colony_name': colony_name,
                'street': street,
                'house_number': house_number,
                'unit': unit,
                'mobile_no':mobile_no,
                'total_floors': total_floors,
                'floor_number': floor_number,
                'owner_name': owner_name,
                'father_name': father_name,
                'area': area,
                'area_code': area_code,
                'longitude': longitude,
                'latitude': latitude,
                'surveyer_id': surveyer_id if surveyer_id else False,
                'installer_id': installer_id if installer_id else False,
                'company_id':company_id,
                'property_image': property_image if property_image else False,
                'property_image1': property_image1 if property_image1 else False,
            }

            property_record.write({
                'survey_line_ids': [(0, 0, survey_line_vals)]
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

    @http.route('/api/create_property', type='http', auth='public', methods=['POST'], csrf=False)
    @check_permission
    def create_property_details(self, **kwargs):
        try:
            data = json.loads(request.httprequest.data or "{}")

            # Extract data safely
            vals = {
                'address_line_1': data.get('address_line_1'),
                'address_line_2': data.get('address_line_2'),
                'mobile_no': data.get('mobile'),
                'colony_name': data.get('colony_name'),
                'house_number': data.get('house_number'),
                'owner_name': data.get('owner_name'),
                'longitude': data.get('longitude'),
                'latitude': data.get('latitude'),
                'surveyer_id': data.get('surveyer_id'),
                'zone_no': data.get('zone_id'),
                'ward_no': data.get('ward_id'),
                'property_status': 'discovered'
            }

            # Create property record
            property_record = request.env['ddn.property.info'].sudo().create(vals)

            response_data = {
                'status': 'success',
                'message': 'Property created successfully',
                'property_id': property_record.id  # optional: return ID of created record
            }
            return Response(
                json.dumps(response_data),
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
        

    # @http.route(['/api/dashboard'], type='http', auth='public', methods=['POST'], csrf=False)
    # @check_permission
    # def dashboard_summary(self, **kwargs):
    #     try:
    #         data = json.loads(request.httprequest.data or "{}")
    #         Property = request.env['ddn.property.info'].sudo()

    #         surveyor_id = data.get('surveyor_id')
    #         company_id = data.get('company_id')

    #         date_from = datetime.strptime(data['date_from'], "%Y/%m/%d")
            
    #         date_to = datetime.strptime(data['date_to'], "%Y/%m/%d")
    #         data = {
                
    #             'uploaded': Property.search_count([('company_id','=',company_id),('surveyer_id','=',surveyor_id),('create_date','>=', date_from),('create_date','<', date_to),('property_status', '=', 'uploaded')]),
    #             'pdf_downloaded': Property.search_count([('company_id','=',company_id),('surveyer_id','=',surveyor_id),('create_date','>=', date_from),('create_date','<', date_to),('property_status', '=', 'pdf_downloaded')]),
    #             'surveyed': Property.search_count([('company_id','=',company_id),('surveyer_id','=',surveyor_id),('create_date','>=', date_from),('create_date','<', date_to),('property_status', '=', 'surveyed')]),
    #             'discovered': Property.search_count([('company_id','=',company_id),('surveyer_id','=',surveyor_id),('create_date','>=', date_from),('create_date','<', date_to),('property_status', '=', 'discovered')]),
    #         }
            

    #         response = {
    #             'status': 'success',
    #             'message': 'Dashboard data fetched successfully',
    #             'data': data
    #         }

    #         return Response(
    #             json.dumps(response),
    #             status=200,
    #             content_type='application/json'
    #         )

    #     except Exception as e:
    #         return Response(
    #             json.dumps({'status': 'error', 'message': 'An error occurred', 'details': str(e)}),
    #             status=500,
    #             content_type='application/json'
    #         )



    @http.route(['/api/dashboard'], type='http', auth='public', methods=['POST'], csrf=False)
    def dashboard_summary(self, **kwargs):
        try:
            data = json.loads(request.httprequest.data or "{}")
            Property = request.env['ddn.property.info'].sudo()

            surveyor_id = data.get('surveyor_id')
            company_id = data.get('company_id')

            # === Today Range ===
            today_from = datetime.combine(date.today(), datetime.min.time())
            today_to = datetime.combine(date.today() + timedelta(days=1), datetime.min.time())

            today_domain = [('company_id', '=', company_id), ('surveyer_id', '=', surveyor_id),
                            ('create_date', '>=', today_from), ('create_date', '<', today_to)]

            today_data = {
                'uploaded': Property.search_count(today_domain + [('property_status', '=', 'uploaded')]),
                'pdf_downloaded': Property.search_count(today_domain + [('property_status', '=', 'pdf_downloaded')]),
                'surveyed': Property.search_count(today_domain + [('property_status', '=', 'surveyed')]),
                'discovered': Property.search_count(today_domain + [('property_status', '=', 'discovered')]),
            }

            # === All / Range Data ===
            if data.get('date_from') and data.get('date_to'):
                date_from = datetime.strptime(data['date_from'], "%Y/%m/%d")
                date_to = datetime.strptime(data['date_to'], "%Y/%m/%d")
            else:
                # Default: from the beginning of time to now
                date_from = datetime.min
                date_to = datetime.now()

            all_domain = [('company_id', '=', company_id), ('surveyer_id', '=', surveyor_id),
                          ('create_date', '>=', date_from), ('create_date', '<', date_to)]

            all_data = {
                'uploaded': Property.search_count(all_domain + [('property_status', '=', 'uploaded')]),
                'pdf_downloaded': Property.search_count(all_domain + [('property_status', '=', 'pdf_downloaded')]),
                'surveyed': Property.search_count(all_domain + [('property_status', '=', 'surveyed')]),
                'discovered': Property.search_count(all_domain + [('property_status', '=', 'discovered')]),
            }

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
