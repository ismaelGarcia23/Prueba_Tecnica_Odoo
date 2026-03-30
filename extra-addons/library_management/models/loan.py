from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta

class LibraryLoan(models.Model):
    _name = 'library.loan'
    _description = 'Préstamo de Libro'
    _inherit = ['mail.thread', 'mail.activity.mixin'] # Para tener el chat abajo

    partner_id = fields.Many2one('res.partner', string="Socio", required=True, domain=[('is_library_member', '=', True)])
    book_id = fields.Many2one('product.template', string="Libro", required=True, domain=[('is_available', '=', True)])
    loan_date = fields.Date(string="Fecha de Préstamo", default=fields.Date.context_today)
    return_date = fields.Date(string="Fecha Límite", compute="_compute_return_date", store=True)
    actual_return_date = fields.Date(string="Fecha de Devolución Real")
    
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('loaned', 'Prestado'),
        ('returned', 'Devuelto'),
        ('overdue', 'Vencido')
    ], string="Estado", default='draft', tracking=True)

    # Punto 5: Cálculo automático de fecha límite (30 días después)
    @api.depends('loan_date')
    def _compute_return_date(self):
        for record in self:
            if record.loan_date:
                record.return_date = record.loan_date + timedelta(days=30)
            else:
                record.return_date = False

    # Botones para cambiar de estado
    def action_confirm_loan(self):
        for record in self:
            if not record.book_id.is_available:
                raise ValidationError("Este libro no está disponible para préstamo.")
            record.book_id.is_available = False
            record.state = 'loaned'

    def action_return_book(self):
        for record in self:
            record.book_id.is_available = True
            record.actual_return_date = fields.Date.context_today(self)
            record.state = 'returned'