from odoo import http
from odoo.http import request

class LibraryPortal(http.Controller):
    # Ruta donde el socio verá sus préstamos
    @http.route(['/my/loans'], type='http', auth="user", website=True)
    def portal_my_loans(self):
        # Buscamos solo los préstamos del socio que tiene la sesión iniciada
        loans = request.env['library.loan'].search([
            ('partner_id', '=', request.env.user.partner_id.id)
        ])
        # Renderizamos la plantilla pasándole los datos
        return request.render("library_management.portal_my_loans_template", {
            'loans': loans,
            'page_name': 'my_loans',
        })