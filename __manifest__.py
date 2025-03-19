{
    'name': 'Material Management',
    'version': '1.0',
    'summary': 'Module untuk mengelola material',
    'author': 'Rinov',
    'category': 'Inventory',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/material_views.xml'
    ],
    'test': ['tests/test_material_api.py'],
    'installable': True,
    'application': True,
    'controllers': [  # Menambahkan controllers agar dikenali oleh Odoo
        'controllers/material_controller.py',
    ],
}
