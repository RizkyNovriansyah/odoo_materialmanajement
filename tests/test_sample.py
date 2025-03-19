from odoo.tests.common import TransactionCase

class TestSample(TransactionCase):
    def setUp(self):
        super(TestSample, self).setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'Test Partner',
            'email': 'test@example.com'
        })
    
    def test_partner_creation(self):
        """Test if the partner is created correctly"""
        self.assertEqual(self.partner.name, 'Test Partner')
        self.assertEqual(self.partner.email, 'test@example.com')
    
    def test_partner_email_change(self):
        """Test if the email can be updated"""
        self.partner.write({'email': 'newemail@example.com'})
        self.assertEqual(self.partner.email, 'newemail@example.com')

    def test_addition(self):
        result = 2 + 3
        self.assertEqual(result, 5)  # ✅ Test akan lulus karena 2 + 3 memang 5

    def test_wrong_addition(self):
        result = 2 + 2
        self.assertEqual(result, 5)  # ❌ Test akan gagal karena 2 + 2 bukan 5