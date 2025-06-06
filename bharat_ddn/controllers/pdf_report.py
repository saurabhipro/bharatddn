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
from PIL import Image, ImageDraw, ImageFont
import logging

_logger = logging.getLogger(__name__)

# Register a custom font (replace with your desired font file path)
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Example path, update as needed
pdfmetrics.registerFont(TTFont("CustomBold", FONT_PATH))

class PdfGeneratorController(http.Controller):

    def generate_ddn_image(self, property_rec, bg_image_path):
        """
        Generate a complete image with text and QR code using original Python coordinates
        """
        try:
            background = Image.open(bg_image_path).convert("RGBA")
            draw = ImageDraw.Draw(background)

            # Fonts
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            center_font = ImageFont.truetype(font_path, 100)
            value_font = ImageFont.truetype(font_path, 70)

            # Property details
            zone = property_rec.zone_id.name or "-"
            locality = property_rec.colony_id.code or "-"
            raw_unit_no = property_rec.unit_no or "-"
            formatted_unit_no = str(raw_unit_no).zfill(4) if raw_unit_no != "-" else "-"

            # Center text (with outline) - this is the only text in the image area
            center_text = f"{zone}-{locality}-{formatted_unit_no}"
            bbox = draw.textbbox((0, 0), center_text, font=center_font)
            text_width = bbox[2] - bbox[0]
            right_x = background.width - 20 - text_width  # Move text 10px to the left
            center_y = 340  # Adjust if needed

            # Draw white outline
            for dx, dy in [(-2,0), (2,0), (0,-2), (0,2), (-2,-2), (-2,2), (2,-2), (2,2)]:
                draw.text((right_x + dx, center_y + dy), center_text, font=center_font, fill='white')
            # Draw main text
            draw.text((right_x, center_y), center_text, font=center_font, fill='black')

            # Table cell positions and widths (adjust if needed)
            value_y = 570  # Increased from 310 to move text down further
            
            zone_box_x, zone_box_y, zone_box_width = 140, 250, 100
            locality_box_x, locality_box_y, locality_box_width = 450, 175, 250
            unit_no_box_x, unit_no_box_y, unit_no_box_width = 900, 175, 155

            # Y coordinate for values (increase this to move text down)

            def draw_centered_text(x, y, w, text, font, fill):
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_x = x + w/2 - text_width/2
                # Draw white outline
                for dx, dy in [(-2,0), (2,0), (0,-2), (0,2), (-2,-2), (-2,2), (2,-2), (2,2)]:
                    draw.text((text_x + dx, y + dy), text, font=font, fill='white')
                # Draw main text
                draw.text((text_x, y), text, font=font, fill=fill)

            # Draw the values in the table
            draw_centered_text(zone_box_x, value_y, zone_box_width, zone, value_font, 'black')
            draw_centered_text(locality_box_x, value_y, locality_box_width, locality, value_font, 'black')
            draw_centered_text(unit_no_box_x, value_y, unit_no_box_width, formatted_unit_no, value_font, 'black')

            # QR code (unchanged)
            qr_box_x, qr_box_y, qr_box_width, qr_box_height = 50, 170, 225, 220
            qr = qrcode.QRCode(
                version=2,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=5,
                border=1
            )
            base_url = property_rec.company_id.website or request.httprequest.host_url
            full_url = f"{base_url}/get/{property_rec.uuid}"
            qr.add_data(full_url)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
            qr_img = qr_img.resize((qr_box_width, qr_box_height), Image.LANCZOS)
            background.alpha_composite(qr_img, (qr_box_x, qr_box_y))

            return background

        except Exception as e:
            print(f"Error generating DDN image: {str(e)}")
            raise

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

        company = request.env.user.company_id
        if not company or not company.plate_background_image:
            return request.not_found("No background image configured for your company.")

        try:
            # Save background image to temporary file
            bg_image_data = base64.b64decode(company.plate_background_image)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_bg:
                bg_image_path = temp_bg.name
                temp_bg.write(bg_image_data)

            # Create a temporary directory to store individual PDFs
            temp_dir = tempfile.mkdtemp()
            individual_pdf_paths = []

            # Process each property separately
            for property_rec in properties:
                try:
                    # Log property info
                    _logger.info(f"Generating PDF for property: ID={property_rec.id}, Zone={getattr(property_rec.zone_id, 'name', '-')}, Locality={getattr(property_rec.colony_id, 'code', '-')}, Unit No={property_rec.unit_no}")

                    # Generate the complete image
                    background = self.generate_ddn_image(property_rec, bg_image_path)
                    
                    # Save the complete image to a temporary file (convert to RGB)
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png", dir=temp_dir) as temp_img:
                        rgb_background = background.convert("RGB")
                        rgb_background.save(temp_img.name, "PNG")
                        img_path = temp_img.name
                    
                    # Create PDF with the complete image
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf", dir=temp_dir) as temp_pdf:
                        pdf_path = temp_pdf.name
                    
                    # Set PDF page size to match background image size
                    c = canvas.Canvas(pdf_path, pagesize=(background.width, background.height))
                    img = ImageReader(img_path)
                    c.drawImage(img, 0, 0, width=background.width, height=background.height)
                    c.save()
                    
                    individual_pdf_paths.append(pdf_path)
                    
                    # Clean up temporary image file
                    os.unlink(img_path)
                    
                except Exception as e:
                    print(f"Error processing property: {str(e)}")
                    continue

            # Merge all PDFs
            merger = PdfMerger()
            for pdf_path in individual_pdf_paths:
                merger.append(pdf_path)

            # Create final PDF
            final_pdf_io = io.BytesIO()
            merger.write(final_pdf_io)
            merger.close()
            final_pdf_io.seek(0)

            # Clean up temporary files
            for pdf_path in individual_pdf_paths:
                try:
                    os.unlink(pdf_path)
                except Exception:
                    pass

            try:
                os.rmdir(temp_dir)
            except Exception:
                pass

            try:
                os.unlink(bg_image_path)
            except Exception:
                pass

            # Set filename based on filters
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
