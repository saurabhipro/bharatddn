import os
import tempfile
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import qrcode
from odoo import http
from odoo.http import request
import base64
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image, ImageDraw, ImageFont
import logging
import zipfile
import shutil
import time
import traceback
from PyPDF2 import PdfMerger

_logger = logging.getLogger(__name__)

# Global configuration

# Configuration Settings
class PDFConfig:
    # Font Configuration
    
    BASE_EXPORT_DIR = '/home/anjli/Anjli/crm/BharatDDN/pdf'  # Base directory for all PDF exports
    FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    CENTER_FONT_SIZE = 150
    VALUE_FONT_SIZE = 70
    BATCH_SIZE = 1000  # Process 20 properties at a time

    # Image Generation Settings
    CENTER_TEXT_Y = 500
    VALUE_TEXT_Y = 570
    TEXT_OUTLINE_OFFSET = 2
    IMAGE_FORMAT = 'JPEG'
    IMAGE_QUALITY = 10     # Increased quality for better clarity
    BACKGROUND_COLOR = 'white'  # Added background color setting
   
    # Table Cell Positions and Dimensions
    TABLE_ROW_Y = 900
    BOX_START_X = 150
    BOX_WIDTH = 250
    BOX_GAP = 350
   
    ZONE_BOX = {
        'x': 200,
        'width': 100
    }
    LOCALITY_BOX = {
        'x': 800,
        'width': 0
    }
    UNIT_NO_BOX = {
        'x': 1200,
        'width': 5
    }
   
    # QR Code Settings
    QR_BOX = {
        'x': 100,
        'y': 270,
        'width': 330,
        'height': 320
    }
    QR_VERSION = 1
    QR_ERROR_CORRECTION = qrcode.constants.ERROR_CORRECT_H
    QR_BOX_SIZE = 20
    QR_BORDER = 1
   
 
# Register the custom font
pdfmetrics.registerFont(TTFont("CustomBold", PDFConfig.FONT_PATH))
 
# Add these global variables at the top of the file, after the imports
class PDFExportStatus:
    _export_status = {}  # Dictionary to store export status for each colony
    _export_folders = {}  # Dictionary to store export folder paths for each colony
    
    @classmethod
    def set_export_status(cls, colony_id, status, folder_path=None):
        cls._export_status[colony_id] = status
        if folder_path:
            cls._export_folders[colony_id] = folder_path
    
    @classmethod
    def get_export_status(cls, colony_id):
        return cls._export_status.get(colony_id, False)
    
    @classmethod
    def get_export_folder(cls, colony_id):
        return cls._export_folders.get(colony_id)

class PdfGeneratorController(http.Controller):
 
    def draw_centered_text(self, x, y, width, text, font, color):
        """Helper function to draw centered text"""
        draw = ImageDraw.Draw(self.current_image)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        x_centered = x + (width - text_width) // 2
        draw.text((x_centered, y), text, font=font, fill=color)
 
    def generate_ddn_image(self, property_rec, bg_image_path):
        """
        Generate a complete image with text and QR code using original Python coordinates
        """
        try:
            # Open and convert background image
            background = Image.open(bg_image_path).convert("RGB")
            # Create a new white background image
            final_image = Image.new('RGB', background.size, PDFConfig.BACKGROUND_COLOR)
            # Paste the background image
            final_image.paste(background, (0, 0))
            draw = ImageDraw.Draw(final_image)
 
            # Store the current image for draw_centered_text to use
            self.current_image = final_image
 
            # Fonts
            center_font = ImageFont.truetype(PDFConfig.FONT_PATH, PDFConfig.CENTER_FONT_SIZE)
            value_font = ImageFont.truetype(PDFConfig.FONT_PATH, PDFConfig.VALUE_FONT_SIZE)
 
            # Property details
            zone = getattr(property_rec.zone_id, 'name', '-') if property_rec.zone_id else '-'
            locality = getattr(property_rec.colony_id, 'code', '-') if property_rec.colony_id else '-'
            raw_unit_no = property_rec.unit_no or "-"
            formatted_unit_no = str(raw_unit_no).zfill(4) if raw_unit_no != "-" else "-"
 
            # Center text (with outline)
            center_text = f"{zone}-{locality}-{formatted_unit_no}"
            bbox = draw.textbbox((0, 0), center_text, font=center_font)
            text_width = bbox[2] - bbox[0]
            right_x = background.width - 20 - text_width
            center_y = PDFConfig.CENTER_TEXT_Y
 
            # Draw white outline
            for dx, dy in [(-PDFConfig.TEXT_OUTLINE_OFFSET,0), (PDFConfig.TEXT_OUTLINE_OFFSET,0),
                          (0,-PDFConfig.TEXT_OUTLINE_OFFSET), (0,PDFConfig.TEXT_OUTLINE_OFFSET),
                          (-PDFConfig.TEXT_OUTLINE_OFFSET,-PDFConfig.TEXT_OUTLINE_OFFSET),
                          (-PDFConfig.TEXT_OUTLINE_OFFSET,PDFConfig.TEXT_OUTLINE_OFFSET),
                          (PDFConfig.TEXT_OUTLINE_OFFSET,-PDFConfig.TEXT_OUTLINE_OFFSET),
                          (PDFConfig.TEXT_OUTLINE_OFFSET,PDFConfig.TEXT_OUTLINE_OFFSET)]:
                draw.text((right_x + dx, center_y + dy), center_text, font=center_font, fill='white')
           
            # Draw main text
            draw.text((right_x, center_y), center_text, font=center_font, fill='black')
 
            # Calculate X positions for each box
            zone_x = PDFConfig.BOX_START_X
            locality_x = zone_x + PDFConfig.BOX_WIDTH + PDFConfig.BOX_GAP
            unit_no_x = locality_x + PDFConfig.BOX_WIDTH + PDFConfig.BOX_GAP
 
            # Draw the values in the table
            self.draw_centered_text(zone_x, PDFConfig.TABLE_ROW_Y, PDFConfig.BOX_WIDTH, zone, value_font, 'white')
            self.draw_centered_text(locality_x, PDFConfig.TABLE_ROW_Y, PDFConfig.BOX_WIDTH, locality, value_font, 'white')
            self.draw_centered_text(unit_no_x, PDFConfig.TABLE_ROW_Y, PDFConfig.BOX_WIDTH, formatted_unit_no, value_font, 'white')
 
            # QR code
            qr = qrcode.QRCode(
                version=PDFConfig.QR_VERSION,
                error_correction=PDFConfig.QR_ERROR_CORRECTION,
                box_size=PDFConfig.QR_BOX_SIZE,
                border=PDFConfig.QR_BORDER
            )
            base_url = property_rec.company_id.website or request.httprequest.host_url
            full_url = f"{base_url}/get/{property_rec.uuid}"
            qr.add_data(full_url)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
            qr_img = qr_img.resize((PDFConfig.QR_BOX['width'], PDFConfig.QR_BOX['height']), Image.LANCZOS)
           
            # Create a white background for QR code
            qr_bg = Image.new('RGB', (PDFConfig.QR_BOX['width'], PDFConfig.QR_BOX['height']), 'white')
            qr_bg.paste(qr_img, (0, 0))
            final_image.paste(qr_bg, (PDFConfig.QR_BOX['x'], PDFConfig.QR_BOX['y']))
 
            return final_image
 
        except Exception as e:
            _logger.error(f"Error generating DDN image for property {getattr(property_rec, 'id', 'unknown')}: {e}", exc_info=True)
            raise
 
    def get_colony_folder(self, colony_id):
        """Create and return colony-specific folder path"""
        colony = request.env['ddn.colony'].sudo().browse(colony_id)
        if not colony.exists():
            raise ValueError(f"Colony with ID {colony_id} not found")
            
        colony_name = colony.name.replace(" ", "_").lower()
        colony_dir = os.path.join(PDFConfig.BASE_EXPORT_DIR, colony_name)
        
        # Remove existing folder if it exists
        if os.path.exists(colony_dir):
            shutil.rmtree(colony_dir)
            
        # Create new folder
        os.makedirs(colony_dir, exist_ok=True)
        
        # Update export status
        PDFExportStatus.set_export_status(colony_id, True, colony_dir)
        
        return colony_dir

    def process_property_batch(self, property_ids, bg_image_path, colony_id=None):
        processed_count = 0
        error_count = 0
        colony_dir = self.get_colony_folder(colony_id) if colony_id else os.path.join(PDFConfig.BASE_EXPORT_DIR, "default")
        os.makedirs(colony_dir, exist_ok=True)

        # Create a single PDF for this batch
        batch_pdf_filename = f"batch_{int(time.time())}.pdf"
        batch_pdf_path = os.path.join(colony_dir, batch_pdf_filename)
        _logger.info(f"Starting batch PDF creation: {batch_pdf_filename}")
        
        # Create canvas for the batch PDF
        c = None
        temp_images = []  # Keep track of temp image files to clean up

        try:
            for property_id in property_ids:
                try:
                    property_rec = request.env['ddn.property.info'].browse(property_id)
                    final_image = self.generate_ddn_image(property_rec, bg_image_path)
                    
                    # Save as temp image
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_img:
                        final_image.save(temp_img.name, PDFConfig.IMAGE_FORMAT, quality=PDFConfig.IMAGE_QUALITY, optimize=True)
                        img_path = temp_img.name
                        temp_images.append(img_path)

                    # If this is the first image, create the canvas
                    if c is None:
                        c = canvas.Canvas(batch_pdf_path, pagesize=final_image.size)

                    # Add image to PDF
                    img = ImageReader(img_path)
                    c.drawImage(img, 0, 0, width=final_image.width, height=final_image.height)
                    c.showPage()  # Add new page for next image
                    
                    property_rec.write({'property_status': 'pdf_downloaded'})
                    processed_count += 1
                    _logger.info(f"Processed Unit No: {property_rec.unit_no}")

                except Exception as e:
                    error_count += 1
                    _logger.error(f"Error processing property {property_id}: {e}", exc_info=True)
                    continue

            # Save and close the PDF
            if c is not None:
                c.save()
                c = None  # Release canvas
                _logger.info(f"Batch PDF generated and saved at: {batch_pdf_path}")

            # Clean up temp images
            for img_path in temp_images:
                try:
                    os.unlink(img_path)
                except Exception as e:
                    _logger.error(f"Error cleaning up temp image {img_path}: {e}")

            _logger.info(f"Memory freed: {len(temp_images)} images and PDF canvas released")
            return processed_count, colony_dir, batch_pdf_path if processed_count > 0 else None

        except Exception as e:
            _logger.error(f"Error in batch processing: {e}", exc_info=True)
            # Clean up resources in case of error
            if c is not None:
                c = None
            for img_path in temp_images:
                try:
                    os.unlink(img_path)
                except:
                    pass
            return processed_count, colony_dir, None

    def merge_pdfs(self, pdf_paths, output_path):
        merger = PdfMerger()
        for pdf in pdf_paths:
            _logger.info(f"Adding to merger: {pdf}")
            merger.append(pdf)
        merger.write(output_path)
        merger.close()
        _logger.info(f"Merged PDF written to: {output_path}")

    @http.route(['/download/ward_properties_pdf'], type='http', auth='user', methods=['GET'], csrf=True)
    def download_ward_properties_pdf(self, **kw):
        _logger.info("Starting PDF generation process")
        ward_id = kw.get('ward_id')
        colony_id = kw.get('colony_id')
        property_id = kw.get('property_id')

        _logger.info(f"Parameters - Ward ID: {ward_id}, Colony ID: {colony_id}, Property ID: {property_id}")

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
            # Ensure base export directory exists
            os.makedirs(PDFConfig.BASE_EXPORT_DIR, exist_ok=True)
            _logger.info(f"Base export directory: {PDFConfig.BASE_EXPORT_DIR}")

            bg_image_data = base64.b64decode(company.plate_background_image)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_bg:
                bg_image_path = temp_bg.name
                temp_bg.write(bg_image_data)
                temp_bg.flush()
                os.fsync(temp_bg.fileno())
                _logger.info(f"Background image saved at: {bg_image_path}")

            # Process properties in batches
            property_ids = [rec.id for rec in properties]
            batch_size = PDFConfig.BATCH_SIZE
            
            _logger.info(f"Total properties to process: {len(property_ids)}")
            total_processed = 0
            output_dir = None
            batch_pdf_paths = []
            
            # Process first batch and send to browser immediately
            first_batch_ids = property_ids[:batch_size]
            _logger.info(f"Processing first batch with {len(first_batch_ids)} properties")
            processed, output_dir, first_batch_pdf = self.process_property_batch(first_batch_ids, bg_image_path, colony_id)
            total_processed += processed

            if first_batch_pdf and os.path.exists(first_batch_pdf):
                _logger.info(f"Sending first batch PDF to browser: {first_batch_pdf}")
                with open(first_batch_pdf, 'rb') as f:
                    return request.make_response(
                        f.read(),
                        headers=[
                            ('Content-Type', 'application/pdf'),
                            ('Content-Disposition', f'inline; filename=first_batch.pdf')
                        ]
                    )

            # If first batch failed, process remaining batches
            remaining_ids = property_ids[batch_size:]
            for i in range(0, len(remaining_ids), batch_size):
                batch_ids = remaining_ids[i:i + batch_size]
                _logger.info(f"Processing batch {i//batch_size + 2} with {len(batch_ids)} properties")
                processed, output_dir, batch_pdf_path = self.process_property_batch(batch_ids, bg_image_path, colony_id)
                total_processed += processed
                
                if batch_pdf_path and os.path.exists(batch_pdf_path):
                    batch_pdf_paths.append(batch_pdf_path)
                    _logger.info(f"Added batch PDF to zip list: {batch_pdf_path}")

            # Create zip for remaining batches
            if batch_pdf_paths:
                zip_filename = f"remaining_batches_{int(time.time())}.zip"
                zip_path = os.path.join(output_dir, zip_filename)
                
                _logger.info(f"Creating zip file with {len(batch_pdf_paths)} PDFs")
                with zipfile.ZipFile(zip_path, 'w') as zipf:
                    for pdf_path in batch_pdf_paths:
                        if os.path.exists(pdf_path):
                            zipf.write(pdf_path, os.path.basename(pdf_path))
                            _logger.info(f"Added to zip: {pdf_path}")

                def file_iterator(file_path, chunk_size=8192):
                    with open(file_path, 'rb') as f:
                        while True:
                            chunk = f.read(chunk_size)
                            if not chunk:
                                break
                            yield chunk

                headers = [
                    ('Content-Type', 'application/zip'),
                    ('Content-Disposition', f'attachment; filename={zip_filename}')
                ]
                return request.make_response(file_iterator(zip_path), headers=headers)
            else:
                _logger.error("No PDFs were successfully created")
                return request.not_found("No PDFs were generated successfully")

        except Exception as e:
            _logger.error(f"An error occurred: {str(e)}")
            return request.not_found(f"An error occurred: {str(e)}")

    @http.route(['/get/export_status'], type='json', auth='user')
    def get_export_status(self, colony_id):
        """Get the export status and folder path for a colony"""
        status = PDFExportStatus.get_export_status(colony_id)
        folder = PDFExportStatus.get_export_folder(colony_id)
        return {
            'status': status,
            'folder': folder
        }

    @http.route(['/get/generated_pdfs/<path:filepath>'], type='http', auth='user')
    def get_generated_pdf(self, filepath, **kw):
        """Serve generated PDF files"""
        try:
            file_path = os.path.join(PDFConfig.BASE_EXPORT_DIR, filepath)
            
            # If it's a directory, list all PDF files in it
            if os.path.isdir(file_path):
                pdf_files = [f for f in os.listdir(file_path) if f.endswith('.pdf')]
                
                html_content = f"""
                <html>
                <body>
                    <h2>PDF Files in {filepath}</h2>
                    <ul>
                """
                
                for pdf_file in pdf_files:
                    pdf_path = os.path.join(filepath, pdf_file)
                    file_url = f"/get/generated_pdfs/{pdf_path}"
                    html_content += f'<li><a href="{file_url}">{pdf_file}</a></li>'
                
                html_content += """
                    </ul>
                </body>
                </html>
                """
                
                return request.make_response(
                    html_content,
                    headers=[('Content-Type', 'text/html')]
                )
            
            # If it's a file, serve it
            elif os.path.isfile(file_path) and file_path.endswith('.pdf'):
                with open(file_path, 'rb') as f:
                    return request.make_response(
                        f.read(),
                        headers=[
                            ('Content-Type', 'application/pdf'),
                            ('Content-Disposition', f'inline; filename={os.path.basename(file_path)}')
                        ]
                    )
                
        except Exception as e:
            _logger.error(f"Error serving file {filepath}: {str(e)}")
        
        return request.not_found("File not found")