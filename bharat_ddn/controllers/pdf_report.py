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
    # @http.route('/download/ward_properties_pdf', type='http', auth='user', methods=['GET'], csrf=True)
    # def download_ward_properties_pdf(self, **kw):
    #     ward_id = kw.get('ward_id')
    #     if not ward_id:
    #         return request.not_found("Ward ID is required.")
        
    #     try:
    #         ward_id = int(ward_id)
    #     except ValueError:
    #         return request.not_found("Invalid Ward ID.")
    #     domain = [('ward_no', '=', ward_id)]
    #     properties = request.env['ddn.property.info'].sudo().search(domain)
    #     if not properties:
    #         return request.not_found("No properties found for this ward.")
        
    #     batch_size = 100
    #     batch_file_paths = []
    #     total_properties = len(properties)
        
    #     current_file_path = os.path.dirname(os.path.abspath(__file__))
    #     bg_image_path = os.path.join(
    #         current_file_path, '..', 'static', 'src', 'img', 'WhatsApp Image 2025-03-27 at 12.10.13 AM.jpeg'
    #     )
    #     if not os.path.exists(bg_image_path):
    #         return request.not_found("Background image not found at %s" % bg_image_path)
        
    #     for batch_start in range(0, total_properties, batch_size):
    #         batch_records = properties[batch_start: batch_start + batch_size]
            
    #         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_batch:
    #             batch_pdf_path = temp_batch.name
            
    #         c = canvas.Canvas(batch_pdf_path, pagesize=landscape(A4))
    #         page_width, page_height = landscape(A4)
    #         bg_image = ImageReader(bg_image_path)
            
    #         for property_rec in batch_records:
    #             c.drawImage(bg_image, 0, 0, width=page_width, height=page_height)
                
    #             zone = property_rec.zone_no.name or "-"
    #             block = property_rec.ward_no.name or "-"
    #             unit_no = property_rec.unit_no or "-"
    #             uuid = property_rec.uuid or "-"
                
    #             c.setFont("Helvetica-Bold", 16)
    #             c.drawString(305, 228, zone)
    #             c.drawString(445, 228, block)
    #             c.drawString(550, 228, unit_no)
                
    #             qr = qrcode.QRCode(
    #                 version=1,
    #                 error_correction=qrcode.constants.ERROR_CORRECT_H,
    #                 box_size=2,  # Adjust as needed
    #                 border=2
    #             )
    #             # qr.add_data(uuid)
    #             base_url = request.httprequest.host_url
    #             full_url = f"{base_url}get/property-details/{uuid}"
    #             qr.add_data(full_url)
    #             qr.make(fit=True)
    #             qr_img = qr.make_image(fill_color="black", back_color="white")
                
    #             qr_buffer = io.BytesIO()
    #             qr_img.save(qr_buffer, format="PNG")
    #             qr_buffer.seek(0)
    #             qr_image = ImageReader(qr_buffer)
                
    #             c.drawImage(qr_image, 350, 330, width=140, height=140)
    #             c.showPage()  # Finalize this page
                
    #         c.save()
    #         batch_file_paths.append(batch_pdf_path)
        
    #     merger = PdfMerger()
    #     for batch_pdf in batch_file_paths:
    #         merger.append(batch_pdf)
        
    #     final_pdf_io = io.BytesIO()
    #     merger.write(final_pdf_io)
    #     merger.close()
    #     final_pdf_io.seek(0)
        
    #     for batch_pdf in batch_file_paths:
    #         try:
    #             os.unlink(batch_pdf)
    #         except Exception:
    #             pass
        
    #     headers = [
    #         ('Content-Type', 'application/pdf'),
    #         ('Content-Disposition', 'attachment; filename="ward_properties.pdf"')
    #     ]
    #     return request.make_response(final_pdf_io.read(), headers=headers)
    


    @http.route('/download/ward_properties_pdf', type='http', auth='user', methods=['GET'], csrf=True)
    def download_ward_properties_pdf(self, **kw):
        ward_id = kw.get('ward_id')
        if not ward_id:
            return request.not_found("Ward ID is required.")
        
        try:
            ward_id = int(ward_id)
        except ValueError:
            return request.not_found("Invalid Ward ID.")
        
        domain = [('ward_no', '=', ward_id)]
        properties = request.env['ddn.property.info'].sudo().search(domain)
        if not properties:
            return request.not_found("No properties found for this ward.")
        
        batch_size = 100
        batch_file_paths = []
        total_properties = len(properties)

        # ✅ Get the background image from the current user's company
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

                    zone = property_rec.zone_no.name or "-"
                    block = property_rec.ward_no.name or "-"
                    unit_no = property_rec.unit_no or "-"
                    uuid = property_rec.uuid or "-"

                    c.setFont("Helvetica-Bold", 16)
                    c.drawString(305, 228, zone)
                    c.drawString(445, 228, block)
                    c.drawString(550, 228, unit_no)

                    qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_H,
                        box_size=2,
                        border=2
                    )
                    # base_url = request.httprequest.host_url
                    base_url = property_rec.company_id.website
                    full_url = f"{base_url}/get/property-details/{uuid}"
                    qr.add_data(full_url)
                    qr.make(fit=True)
                    qr_img = qr.make_image(fill_color="black", back_color="white")

                    qr_buffer = io.BytesIO()
                    qr_img.save(qr_buffer, format="PNG")
                    qr_buffer.seek(0)
                    qr_image = ImageReader(qr_buffer)

                    c.drawImage(qr_image, 350, 330, width=140, height=140)
                    c.showPage()

                c.save()
                batch_file_paths.append(batch_pdf_path)

            # Merge all PDFs
            merger = PdfMerger()
            for batch_pdf in batch_file_paths:
                merger.append(batch_pdf)

            final_pdf_io = io.BytesIO()
            merger.write(final_pdf_io)
            merger.close()
            final_pdf_io.seek(0)

            # Cleanup batch files
            for batch_pdf in batch_file_paths:
                try:
                    os.unlink(batch_pdf)
                except Exception:
                    pass

            # ✅ Cleanup temp background image
            try:
                os.unlink(bg_image_path)
            except Exception:
                pass

            headers = [
                ('Content-Type', 'application/pdf'),
                ('Content-Disposition', 'attachment; filename="ward_properties.pdf"')
            ]
            return request.make_response(final_pdf_io.read(), headers=headers)

        except Exception as e:
            return request.not_found(f"An error occurred: {str(e)}")



