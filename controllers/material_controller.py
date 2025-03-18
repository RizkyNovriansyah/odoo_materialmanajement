from odoo import http
from odoo.http import request, Response
import json

class MaterialController(http.Controller):
    
    @http.route('/web/material/',website=True,auth='public')
    def web(self, **kw):
        return "Hello, World"

    @http.route('/api/materials/supplier', type='http', auth='public', methods=['GET'], csrf=False)
    def material_supplier(self):
        try:
            suppliers = request.env['res.partner'].sudo().search([])
            supplier_list = [
                {'id': supplier.id, 'name': supplier.name}
                for supplier in suppliers
            ]

            return Response(
                json.dumps({'suppliers': supplier_list}),
                content_type='application/json',
                status=200
            )

        except Exception as e:
            return Response(
                json.dumps({'error': str(e)}),
                content_type='application/json',
                status=500
            )
        
    @http.route('/api/materials/type', type='http', auth='public', methods=['GET'], csrf=False)
    def material_type(self):
        try:
            material_types = [
                {'type': 'fabric', 'name': 'Fabric'},
                {'type': 'jeans', 'name': 'Jeans'},
                {'type': 'cotton', 'name': 'Cotton'}
            ]

            return Response(json.dumps({"material_type":material_types}), content_type='application/json', status=200)

        except Exception as e:
            return request.make_response(json.dumps({'message': e}), headers=[('Content-Type', 'application/json')])
        
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

    # Endpoint untuk menambahkan material baru
    @http.route('/api/materials', type='json', auth='public', methods=['POST'], csrf=False)
    def create_material(self):
        try:
            post = request.jsonrequest 
            print("post",post)
            # Pastikan semua field yang diperlukan tersedia
            required_fields = ["name", "code", "material_type", "buy_price", "supplier_id"]
            missing_fields = [field for field in required_fields if field not in post]

            if missing_fields:
                return {"error": f"Missing required fields: {', '.join(missing_fields)}"}
            
            if post['buy_price'] < 100:
                return {'error': 'Material buy price must be at least 100'}

            # Buat record baru di model 'material.management'
            material = request.env["material.management"].sudo().create({
                "name": post["name"],
                "code": post["code"],
                "material_type": post["material_type"],
                "buy_price": float(post["buy_price"]),
                "supplier_id": int(post["supplier_id"])
            })

            return {
                "message": "Material created successfully",
                "id": material.id,
                "name": material.name
            }

        except Exception as e:
            return {"error": str(e)}

    # Endpoint untuk memperbarui material
    @http.route('/api/materials/<int:material_id>', type='json', auth='public', methods=['PUT'], csrf=False)
    def update_material(self, material_id):
        try:
            data = request.jsonrequest  # Ambil data JSON dari body request
            print("update data", data)  # Debugging

            # Ambil material berdasarkan ID
            material = request.env['material.management'].sudo().browse(material_id)

            if not material.exists():
                return {'error': 'Material not found'}
            
            if data['buy_price'] < 100:
                return {'error': 'Material buy price must be at least 100'}

            # Update hanya field yang dikirim dalam request
            material.write({key: value for key, value in data.items() if key in material._fields})

            return {
                'message': 'Material updated successfully',
                'id': material.id,
                'updated_fields': list(data.keys())
            }

        except Exception as e:
            return {'error': str(e)}
