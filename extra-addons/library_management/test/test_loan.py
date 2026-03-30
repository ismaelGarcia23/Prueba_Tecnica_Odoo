from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestLibraryLoan(TransactionCase):
    def setUp(self):
        super().setUp()
        self.partner = self.env['res.partner'].create({'name': 'Socio Test', 'is_library_member': True})
        self.book = self.env['product.template'].create({'name': 'Libro Test', 'is_available': True})

    def test_loan_limit(self):
        """Prueba que el límite de 5 libros funcione"""
        # Creamos 5 préstamos
        for i in range(5):
            self.env['library.loan'].create({
                'partner_id': self.partner.id,
                'book_id': self.book.id,
                'state': 'loaned'
            })
        # El sexto debe lanzar error
        with self.assertRaises(ValidationError):
            self.env['library.loan'].create({
                'partner_id': self.partner.id,
                'book_id': self.book.id,
                'state': 'loaned'
            })