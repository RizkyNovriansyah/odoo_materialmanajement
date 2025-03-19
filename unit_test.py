import unittest
import requests

BASE_URL = "http://localhost:8069/api/materials"

class TestMaterialsAPI(unittest.TestCase):
    material_id = None
    supplier_id = None
    type_code = None

    def test_01_get_suppliers_list(self):
        """Mengembalikan Supplier List"""
        response = requests.get(f"{BASE_URL}/supplier")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertGreater(len(data["results"]), 0)
        TestMaterialsAPI.supplier_id = data["results"][0]["id"]

    def test_02_get_material_type_list(self):
        """Mengembalikan Type list"""
        response = requests.get(f"{BASE_URL}/type")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertGreater(len(data["results"]), 0)
        TestMaterialsAPI.type_code = data["results"][0]["type"]

    def test_03_create_material_fail(self):
        """Material Baru. buy price < 100"""
        payload = {
            "name": "Rin7",
            "code": "R1237",
            "material_type": TestMaterialsAPI.type_code,
            "buy_price": 50,
            "supplier_id": TestMaterialsAPI.supplier_id
        }
        response = requests.post(BASE_URL, json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertIn("error", data.get("result", {}))
        self.assertEqual(data["result"]["error"], "Material buy price must be at least 100")

    def test_04_create_material(self):
        """Material baru. buy price => 100"""
        payload = {
            "name": "Rin7",
            "code": "R1237",
            "material_type": TestMaterialsAPI.type_code,
            "buy_price": 100,
            "supplier_id": TestMaterialsAPI.supplier_id
        }
        response = requests.post(BASE_URL, json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("id", data.get("result", {}))
        TestMaterialsAPI.material_id = data["result"]["id"]
        self.assertEqual(data["result"]["name"], payload["name"])

    
    def test_05_get_materials_list(self):
        """Material List"""
        response = requests.get(BASE_URL)
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertIn("results", data)
        self.assertGreater(len(data["results"]), 0)

    def test_06_get_material_by_id(self):
        """Get Material by ID"""
        self.assertIsNotNone(TestMaterialsAPI.material_id, "Material ID tidak tersedia")
        response = requests.get(f"{BASE_URL}/{TestMaterialsAPI.material_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertIn("results", data)

    def test_07_update_material_fail(self):
        """Update Material buy price < 100"""
        self.assertIsNotNone(TestMaterialsAPI.material_id, "Material ID tidak tersedia")
        payload = {
            "name": "Rinov",
            "code": "RIN123",
            "buy_price": 10,
            "material_type": TestMaterialsAPI.type_code,
            "supplier_id": TestMaterialsAPI.supplier_id
        }
        response = requests.post(BASE_URL, json=payload)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("error", data.get("result", {}))
        self.assertEqual(data["result"]["error"], "Material buy price must be at least 100")

    def test_08_update_material_fail(self):
        """Update Material buy price > 100"""
        self.assertIsNotNone(TestMaterialsAPI.material_id, "Material ID tidak tersedia")
        payload = {
            "name": "Rinov",
            "code": "RIN123",
            "buy_price": 210,
            "material_type": TestMaterialsAPI.type_code,
            "supplier_id": TestMaterialsAPI.supplier_id
        }
        response = requests.put(f"{BASE_URL}/{TestMaterialsAPI.material_id}", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertIn("message", data.get("result", {}))
        self.assertEqual(data["result"]["message"], "Material updated successfully")

    def test_09_delete_material(self):
        """Delete Matrial"""
        self.assertIsNotNone(TestMaterialsAPI.material_id, "Material ID tidak tersedia")
        response = requests.delete(f"{BASE_URL}/{TestMaterialsAPI.material_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertIn("message", data)
        self.assertEqual(data["message"], "Material deleted")


if __name__ == "__main__":
    unittest.main()
