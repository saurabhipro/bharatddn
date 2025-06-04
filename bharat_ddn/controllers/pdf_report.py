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
from reportlab.lib.colors import white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register a custom font (replace with your desired font file path)
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Example path, update as needed
pdfmetrics.registerFont(TTFont("CustomBold", FONT_PATH))

class PdfGeneratorController(http.Controller):

    @http.route(['/download/ward_properties_pdf'], type='http', auth='user', methods=['GET'], csrf=True)
    def download_ward_properties_pdf(self, **kw):
        print("function is working fine")
        ward_id = kw.get('ward_id')
        colony_id = kw.get('colony_id')
        property_id = kw.get('property_id')

        # Validate property_id if provided
        if property_id:
            try:
                property_id = int(property_id)
            except ValueError:
                return request.not_found("Invalid Property ID.")

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
        if property_id:
            domain = [('id', '=', property_id)]
        else:
            if ward_id:
                domain.append(('ward_id', '=', ward_id))
            if colony_id:
                domain.append(('colony_id', '=', colony_id))

        properties = request.env['ddn.property.info'].sudo().search(domain)
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

                    # Format house number to 4 digits
                    raw_unit_no = property_rec.zone_id.name or "-"
                    if raw_unit_no != "-":
                        formatted_unit_no = str(raw_unit_no).zfill(4)
                    else:
                        formatted_unit_no = "-"

                    # Draw the big black zone-locality-unit_no in the center
                    zone = property_rec.zone_id.name or "-"
                    locality = property_rec.colony_id.code or "-"
                    center_text = f"{zone}-{locality}-{formatted_unit_no}"

                    center_x = page_width - 50
                    center_y = 320
                    c.setFont("CustomBold", 65)
                    c.setFillColorRGB(1, 1, 1)  # White
                    for dx, dy in [(-2,0), (2,0), (0,-2), (0,2), (-2,-2), (-2,2), (2,-2), (2,2)]:
                        c.drawRightString(center_x+dx, center_y+dy, center_text)

                    c.setFillColorRGB(0, 0, 0)  # Black
                    c.drawRightString(center_x, center_y, center_text)

                    # Set font and color for white text in red section
                    c.setFont("CustomBold", 40)  # Larger font for red section
                    c.setFillColor(white)

                    # Define box positions and widths (adjust these as per your template)
                    zone_box_x, zone_box_y, zone_box_width = 40, 175, 180
                    locality_box_x, locality_box_y, locality_box_width = 280, 175, 250
                    unit_no_box_x, unit_no_box_y, unit_no_box_width = 610, 175, 155

                    # Get dynamic values
                    zip = property_rec.company_id.zip or "-"
                    colony = property_rec.colony_id.code or "-"

                    # Centered text in each box
                    c.drawCentredString(zone_box_x + zone_box_width / 2, zone_box_y, zone)
                    c.drawCentredString(locality_box_x + locality_box_width / 2, locality_box_y, colony)
                    c.drawCentredString(unit_no_box_x + unit_no_box_width / 2, unit_no_box_y, formatted_unit_no)

                    qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_H,
                        box_size=2,
                        border=2
                    )
                    base_url = property_rec.company_id.website or request.httprequest.host_url
                    full_url = f"{base_url}/get/{property_rec.uuid}"
                    
                    qr.add_data(full_url)
                    qr.make(fit=True)
                    qr_img = qr.make_image(fill_color="black", back_color="white")

                    qr_buffer = io.BytesIO()
                    qr_img.save(qr_buffer, format="PNG")
                    qr_buffer.seek(0)
                    qr_image = ImageReader(qr_buffer)

                    # Draw QR code centered in its box (now fills the box)
                    qr_box_x, qr_box_y, qr_box_width, qr_box_height = 45, 350, 170, 160
                    qr_size = min(qr_box_width, qr_box_height)
                    qr_x = qr_box_x - 9
                    qr_y = qr_box_y - 15 # Move QR code slightly towards the bottom
                    c.drawImage(qr_image, qr_x, qr_y, width=qr_size, height=qr_size)

                    c.setFillColorRGB(0, 0, 0)  # Reset color if needed for other elements

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
