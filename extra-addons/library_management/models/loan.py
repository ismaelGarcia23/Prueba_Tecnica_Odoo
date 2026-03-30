from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta

class LibraryLoan(models.Model):
    _name = 'library.loan'
    _description = 'Préstamo de Libro'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    partner_id = fields.Many2one(
        'res.partner', 
        string="Socio", 
        required=True, 
        domain=[('is_library_member', '=', True)],
        tracking=True
    )
    book_id = fields.Many2one(
        'product.template', 
        string="Libro", 
        required=True, 
        domain=[('is_available', '=', True)],
        tracking=True
    )
    loan_date = fields.Date(
        string="Fecha de Préstamo", 
        default=fields.Date.context_today,
        tracking=True
    )
    return_date = fields.Date(
        string="Fecha Límite", 
        compute="_compute_return_date", 
        store=True,
        tracking=True
    )
    actual_return_date = fields.Date(
        string="Fecha de Devolución Real",
        tracking=True
    )
    
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('loaned', 'Prestado'),
        ('returned', 'Devuelto'),
        ('overdue', 'Vencido')
    ], string="Estado", default='draft', tracking=True)

    
    @api.depends('loan_date')
    def _compute_return_date(self):
        for record in self:
            if record.loan_date:
                record.return_date = record.loan_date + timedelta(days=30)
            else:
                record.return_date = False

    # Lógica para Confirmar Préstamo
    def action_confirm_loan(self):
        for record in self:
            if not record.book_id.is_available:
                raise ValidationError("Este libro no está disponible para préstamo.")
            # Cambiamos disponibilidad en el libro
            record.book_id.is_available = False
            record.state = 'loaned'

    # Lógica para Devolver Libro
    def action_return_book(self):
        for record in self:
            record.book_id.is_available = True
            record.actual_return_date = fields.Date.context_today(self)
            record.state = 'returned'

   
    @api.constrains('partner_id', 'state')
    def _check_loan_limit(self):
        for record in self:
            if record.state == 'loaned':
                loan_count = self.env['library.loan'].search_count([
                    ('partner_id', '=', record.partner_id.id),
                    ('state', '=', 'loaned')
                ])
                if loan_count > 5:
                    raise ValidationError(
                        f"El socio {record.partner_id.name} ya tiene 5 libros en su poder. "
                        "Debe devolver uno antes de solicitar otro."
                    )

    
    @api.model
    def _cron_check_overdue_loans(self):
        """Busca préstamos que pasaron su fecha límite y no han sido devueltos"""
        today = fields.Date.context_today(self)
        
        overdue_loans = self.search([
            ('state', '=', 'loaned'),
            ('return_date', '<', today)
        ])
        if overdue_loans:

            overdue_loans.write({'state': 'overdue'})