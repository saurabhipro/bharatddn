import io
import os
import tempfile
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import qrcode
from PyPDF2 import PdfMerger
from odoo import http
from odoo.http import request
from odoo import http
from odoo.http import request
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.utils import ImageReader
from PyPDF2 import PdfMerger
import qrcode
import os
import io
import base64
import tempfile




class PdfGeneratorController(http.Controller):

    @http.route(['/download/ward_properties_pdf'], type='http', auth='user', methods=['GET'], csrf=True)
    def download_ward_properties_pdf(self, **kw):
        print("function is working fine")
        ward_id = kw.get('ward_id')
        colony_id = kw.get('colony_id')

        # Validate ward_id if provided
        if ward_id:
            try:
                ward_id = int(ward_id)
            except ValueError:
                return request.not_found("Invalid Ward ID.")

        # Validate colony_id if provided
        if colony_id:
            try:
                colony_id = int(colony_id)
            except ValueError:
                return request.not_found("Invalid Colony ID.")

        # Construct search domain
        domain = []
        if ward_id:
            domain.append(('ward_id', '=', ward_id))
        if colony_id:
            domain.append(('colony_id', '=', colony_id))

        properties = request.env['ddn.property.info'].sudo().search(domain,limit=100)
        if not properties:
            return request.not_found("No properties found for the given criteria.")

        batch_size = 100
        batch_file_paths = []
        total_properties = len(properties)

        company = request.env.user.company_id
        if not company or not company.plate_background_image:
            return request.not_found("No background image configured for your company.")

        try:
            plate_background_image_data = base64.b64decode(company.plate_background_image)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpeg") as temp_img_file:
                temp_img_file.write(plate_background_image_data)
                bg_image_path = temp_img_file.name
        except Exception as e:
            return request.not_found(f"Error loading background image: {str(e)}")

        try:
            for batch_start in range(0, total_properties, batch_size):
                batch_records = properties[batch_start: batch_start + batch_size]

                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_batch:
                    batch_pdf_path = temp_batch.name

                c = canvas.Canvas(batch_pdf_path, pagesize=landscape(A4))
                page_width, page_height = landscape(A4)
                bg_image = ImageReader(bg_image_path)

                for property_rec in batch_records:
                    c.drawImage(bg_image, 0, 0, width=page_width, height=page_height)

                    zip = property_rec.company_id.zip or "-"
                    colony = property_rec.colony_id.name or "-"
                    unit_no = property_rec.unit_no or "-"
                    uuid = property_rec.uuid or "-"

                    c.setFont("Helvetica-Bold", 16)
                    c.drawString(130, 166, zip)
                    c.drawString(365, 166, colony)
                    c.drawString(700, 166, unit_no)

                    qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_H,
                        box_size=2,
                        border=2
                    )
                    base_url = property_rec.company_id.website or request.httprequest.host_url
                    full_url = f"{base_url}/get/{uuid}"
                    
                    qr.add_data(full_url)
                    qr.make(fit=True)
                    qr_img = qr.make_image(fill_color="black", back_color="white")

                    qr_buffer = io.BytesIO()
                    qr_img.save(qr_buffer, format="PNG")
                    qr_buffer.seek(0)
                    qr_image = ImageReader(qr_buffer)

                    c.drawImage(qr_image, 63, 353, width=140, height=140)
                    c.showPage()

                c.save()
                batch_file_paths.append(batch_pdf_path)

            merger = PdfMerger()
            for batch_pdf in batch_file_paths:
                merger.append(batch_pdf)

            final_pdf_io = io.BytesIO()
            merger.write(final_pdf_io)
            merger.close()
            final_pdf_io.seek(0)

            for batch_pdf in batch_file_paths:
                try:
                    os.unlink(batch_pdf)
                except Exception:
                    pass

            try:
                os.unlink(bg_image_path)
            except Exception:
                pass

            filename = "ward_properties.pdf"
            if ward_id and colony_id:
                filename = f"ward_{ward_id}_colony_{colony_id}_properties.pdf"
            elif ward_id:
                filename = f"ward_{ward_id}_properties.pdf"
            elif colony_id:
                filename = f"colony_{colony_id}_properties.pdf"

            headers = [
                ('Content-Type', 'application/pdf'),
                ('Content-Disposition', f'attachment; filename="{filename}"')
            ]
            return request.make_response(final_pdf_io.read(), headers=headers)

        except Exception as e:
            return request.not_found(f"An error occurred: {str(e)}")
