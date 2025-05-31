from odoo import models, fields, api
from odoo.exceptions import ValidationError
import base64
import csv
from io import StringIO, BytesIO
import os

class PropertyImportWizard(models.TransientModel):
    _name = 'property.import.wizard'
    _description = 'Wizard to import property data'

    data_file = fields.Binary('CSV or Excel File', required=True)
    filename = fields.Char('Filename')

    def action_import(self):
        if not self.data_file:
            raise ValidationError('Please upload a CSV or Excel file.')
        if not self.filename:
            raise ValidationError('Filename is missing.')
        ext = os.path.splitext(self.filename)[-1].lower()
        try:
            file_content = base64.b64decode(self.data_file)
            if ext == '.csv':
                csvfile = StringIO(file_content.decode('utf-8'))
                reader = csv.DictReader(csvfile)
                rows = list(reader)
            elif ext in ('.xls', '.xlsx'):
                try:
                    import pandas as pd
                except ImportError:
                    raise ValidationError('pandas library is required for Excel import. Please install it.')
                df = pd.read_excel(BytesIO(file_content))
                rows = df.to_dict(orient='records')
            else:
                raise ValidationError('Unsupported file type. Please upload a .csv, .xls, or .xlsx file.')
            for row in rows:
                self.env['property.id.data'].create({
                    'property_id': row.get('property_id'),
                    'owner_name': row.get('owner_name'),
                    'address': row.get('address'),
                    'mobile_no': row.get('mobile_no'),
                    'currnet_tax': row.get('currnet_tax'),
                    'total_amount': row.get('total_amount'),
                })
        except Exception as e:
            raise ValidationError('Import failed: %s' % str(e))
        return {'type': 'ir.actions.act_window_close'} 