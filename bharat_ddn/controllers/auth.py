from .main import *

SECRET_KEY = 'secret'

class JWTAuthController(http.Controller):


    """ OTP SENT AND SIGN UP """
    @http.route('/api/auth/request_otp', type='http', auth='public', methods=['POST'], csrf=False)
    def request_otp(self, **kwargs):
        data = json.loads(request.httprequest.data or "{}")
        mobile = data.get('mobile')
        if not mobile:
            return Response(json.dumps({'error': 'Mobile number is missing'}), status=400, content_type='application/json' )

        user = request.env['res.users'].sudo().search([('mobile', '=', mobile)], limit=1)
        
        if not user:           
            # user_vals = {
            #     'name': f"demo{user.id+1}",
            #     'mobile': mobile,
            #     'login': f"demo{user.id+1}",
            #     'active': True,
            #     'company_id': 1,
            #     'company_ids': [(4, 1)],
            #     'groups_id': [(6, 0, [request.env.ref('base.group_user').id, request.env.ref('jwt_mobile_auth.surveyor_group_ddn').id])],  # Assigning the user to the basic user group
            # }
            return Response(json.dumps({'error': 'Surveyor Not Register'}), status=400, content_type='application/json')
        
        check_surveyor = user.is_surveyor
        if not check_surveyor:
            return Response(json.dumps({'error': 'Access restricted: You must be assigned to the Surveyor group to proceed.'}), status=400, content_type='application/json')

        existing_otp = request.env['mobile.otp'].sudo().search([('mobile', '=', mobile)])
        if existing_otp:
            existing_otp.unlink()

        otp_code = str(random.randint(1000, 9999))
        expire_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)

        request.env['mobile.otp'].sudo().create({
            'mobile': mobile,
            'user_id': user.id,
            'otp': otp_code,
            'expire_date': expire_time.strftime('%Y-%m-%d %H:%M:%S'),
        })

        try:
            template_url = request.env['ir.config_parameter'].sudo().get_param('otp_url')
            if not template_url or not isinstance(template_url, str):
                # If template_url is not valid, use hardcoded OTP
                return Response(json.dumps({
                    'message': 'OTP sent successfully (simulated)',
                    'details': 'Using fallback OTP due to invalid template URL',
                    'otp': 1000
                }), status=200, content_type='application/json')

            # Remove any 'f' prefix if it exists in the template_url
            if template_url.startswith('f"') or template_url.startswith("f'"):
                template_url = template_url[2:-1]  # Remove f" and the closing quote

            api_url = template_url.format(mobile=mobile, otp_code=otp_code)
            response = requests.get(api_url)
            if response.status_code == 200 and 'ERR' not in response.text:
                # API worked successfully, use actual OTP
                return Response(json.dumps({
                    'message': 'OTP sent successfully',
                    'details': response.text,
                    'otp': otp_code
                }), status=200, content_type='application/json')
            else:
                # API failed or returned error, use hardcoded OTP
                return Response(json.dumps({
                    'message': 'OTP sent successfully (simulated)',
                    'details': 'Using fallback OTP due to API failure',
                    'otp': 1000
                }), status=200, content_type='application/json')
        except Exception as e:
            # Any exception, use hardcoded OTP
            return Response(json.dumps({
                'message': 'OTP sent successfully (simulated)',
                'details': 'Using fallback OTP due to API error',
                'otp': 1000
            }), status=200, content_type='application/json')
               
    """ LOGIN """
    @http.route('/api/auth/login', type='http', auth='none', methods=['POST'], csrf=False)
    def login(self, **kwargs):
        data = json.loads(request.httprequest.data or "{}")
        mobile = data.get('mobile')
        otp_input = data.get('otp_input')

        if not mobile or not otp_input:
            return Response(json.dumps({'error': 'Mobile number or OTP is missing'}), status=400, content_type='application/json')

        otp_record = request.env['mobile.otp'].sudo().search([
            ('mobile', '=', mobile),
            ('otp', '=', otp_input)
        ], limit=1)
        print("OTP Record - ", otp_record)
        if not otp_record:
            return Response( json.dumps({'error': 'Invalid OTP'}), status=400, content_type='application/json' )

        expire_date = otp_record.expire_date
        if datetime.datetime.utcnow() > expire_date:
            otp_record.unlink()
            return Response(json.dumps({'error': 'OTP expired'}),status=400, content_type='application/json')

        user = otp_record.user_id
        print("User - ", user)
        otp_record.unlink()

        payload = {
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        request.env['jwt.token'].sudo().create({'user_id': user.id, 'token': token})
        return Response(json.dumps({'user_id': user.id, 'company_id': user.company_id.id, 'token': token}), status=200, content_type='application/json' )

    """ API CRUD """
    @http.route('/api/get_contacts', type='json', auth='none', methods=['POST'], csrf=False)
    def get_contacts(self, **kwargs):
        try:
            user_id = check_permission(request.httprequest.headers.get('Authorization'))
            if user_id :
                contacts = request.env['res.partner'].sudo().search([])
                contact_data = []
                for contact in contacts:
                    contact_data.append({
                        'name': contact.name,
                        'phone': contact.phone,
                        'email': contact.email,
                        'company': contact.company_id.name if contact.company_id else ''
                    })

                return {'contacts': contact_data}

        except jwt.ExpiredSignatureError:
            raise AccessError('JWT token has expired')
        except jwt.InvalidTokenError:
            raise AccessError('Invalid JWT token')
        
    @http.route('/api/user_profile/<int:id>', type='http', auth='public', methods=['GET', 'POST'], csrf=False)
    @check_permission
    def user_profile(self, id, **kwargs):
        try:
            user = request.env['res.users'].sudo().search([('id', '=', id)], limit=1)

            if not user:
                return Response(
                    json.dumps({'status': 'error', 'message': f'User with id {id} not found.'}),
                    status=404,
                    content_type='application/json'
                )

            if request.httprequest.method == 'GET':
                user_data = {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email,
                    'mobile': user.mobile,
                    'image_1920': str(user.image_1920)  # base64
                }
                return Response(
                    json.dumps({'status': 'success', 'message': 'User profile fetched successfully', 'data': user_data}),
                    status=200,
                    content_type='application/json'
                )

            elif request.httprequest.method == 'POST':
                data = json.loads(request.httprequest.data or "{}")
                vals = {}

                if 'name' in data:
                    vals['name'] = data['name']
                if 'mobile' in data:
                    vals['mobile'] = data['mobile']
                if 'email' in data:
                    vals['email'] = data['email']
                if 'image_1920' in data:
                    vals['image_1920'] = data['image_1920']

                if not vals:
                    return Response(
                        json.dumps({'status': 'error', 'message': 'No valid fields to update.'}),
                        status=400,
                        content_type='application/json'
                    )

                user.sudo().write(vals)

                return Response(
                    json.dumps({'status': 'success', 'message': 'User profile updated successfully', 'updated_fields': list(vals.keys())}),
                    status=200,
                    content_type='application/json'
                )

        except Exception as e:
            return Response(
                json.dumps({'status': 'error', 'message': 'An error occurred', 'details': str(e)}),
                status=500,
                content_type='application/json'
            )