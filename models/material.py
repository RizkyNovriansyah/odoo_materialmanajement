from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class MaterialData(models.Model):
    _name = 'material.management'  # Nama teknis model
    _description = 'Material Management'

    name = fields.Char(string="Material Name", required=True)
    code = fields.Char(string="Material Code", required=True, unique=True)
    material_type = fields.Selection([
        ('fabric', 'Fabric'),
        ('jeans', 'Jeans'),
        ('cotton', 'Cotton')
    ], string="Material Type", required=True)
    buy_price = fields.Float(string="Material Buy Price", required=True)
    supplier_id = fields.Many2one('res.partner', string="Related Supplier", required=True)

    @api.constrains('buy_price')
    def _check_buy_price(self):
        for record in self:
            if record.buy_price < 100:
                raise ValidationError(_("Material buy price must be at least 100."))