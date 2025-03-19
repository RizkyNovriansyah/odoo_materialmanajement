from odoo.tests.common import TransactionCase

class TestSample(TransactionCase):

    def setUp(self):
        """Setup sebelum setiap test dijalankan"""
        super().setUp()
        
        # Inisialisasi model material.management
        self.material_model = self.env['material.management']
        
        # Buat partner (supplier) untuk keperluan test
        self.partner = self.env['res.partner'].create({
            'name': 'Test Partner',
            'email': 'test@example.com'
        })

        self.material = self.material_model.create({
            'name': 'Denim',
            'code': 'D123',
            'material_type': 'jeans',
            'buy_price': 150,
            'supplier_id': self.partner.id
        })

    def test_01_create_material(self):
        """Test apakah material telah dibuat dengan benar"""
        self.assertTrue(self.material, "Material should be created")
        self.assertEqual(self.material.name, 'Denim', "Material name should be 'Denim'")
        self.assertEqual(self.material.code, 'D123', "Material code should be 'D123'")
        self.assertEqual(self.material.buy_price, 150, "Material price should be 150")
        self.assertEqual(self.material.supplier_id.id, self.partner.id, "Supplier ID should match")

    def test_02_get_material(self):
        """Test mengambil daftar material yang ada"""
        materials = self.material_model.search([])
        self.assertGreater(len(materials), 0, "There should be at least one material in the system")

    def test_03_update_material(self):
        """Test memperbarui data material"""
        # Update harga beli material
        self.material.write({'buy_price': 200})
        
        # Refresh data dari database
        self.material.invalidate_cache()
        
        # Pastikan nilai sudah diperbarui
        self.assertEqual(self.material.buy_price, 200, "Material price should be updated to 200")

    def test_04_delete_material(self):
        """Test menghapus material"""
        # Simpan ID sebelum dihapus
        material_id = self.material.id
        
        # Hapus material
        self.material.unlink()

        # Cek apakah masih ada di database
        deleted_material = self.material_model.browse(material_id)
        self.assertFalse(deleted_material.exists(), "Material should be deleted")
