from odoo import http
from odoo.http import request, Response
import json

class MaterialController(http.Controller):
    
    @http.route('/web/material/',website=True,auth='public')
    def web(self, **kw):
        return "Hello, World"

    # Endpoint untuk mendapatkan semua data material
    @http.route('/api/materials', type='http', auth='public', methods=['GET'], csrf=False)
    def get_materials(self, **kwargs):
        materials = request.env['material.management'].sudo().search([])
        data = []
        for material in materials:
            data.append({
                'id': material.id,
                'name': material.name,
                'code': material.code,
                'material_type': material.material_type,
                'buy_price': material.buy_price,
                'supplier_id': material.supplier_id.id if material.supplier_id else None,
            })
        return Response(json.dumps(data), content_type='application/json', status=200)

    # Endpoint untuk mendapatkan data material berdasarkan ID
    @http.route('/api/materials/<int:material_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_material_by_id(self, material_id, **kwargs):
        material = request.env['material.management'].sudo().browse(material_id)
        if not material.exists():
            return Response(json.dumps({'error': 'Material not found'}), content_type='application/json', status=404)

        data = {
            'id': material.id,
            'name': material.name,
            'code': material.code,
            'material_type': material.material_type,
            'buy_price': material.buy_price,
            'supplier_id': material.supplier_id.id if material.supplier_id else None,
        }
        return Response(json.dumps(data), content_type='application/json', status=200)


    # Endpoint untuk menghapus material
    @http.route('/api/materials/<int:material_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def delete_material(self, material_id, **kwargs):
        material = request.env['material.management'].sudo().browse(material_id)
        if not material.exists():
            return request.make_response(json.dumps({'error': 'Material not found'}), headers=[('Content-Type', 'application/json')])

        material.unlink()
        return request.make_response(json.dumps({'message': 'Material deleted'}), headers=[('Content-Type', 'application/json')])
