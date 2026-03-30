from odoo import models, fields, api
from datetime import date

class ProductTemplate(models.Model):
    _inherit = 'product.template' # Heredamos de la ficha de producto estándar 

    # Campos solicitados en la prueba 
    author = fields.Char(string="Autor")
    isbn = fields.Char(string="ISBN")
    published_date = fields.Date(string="Fecha de Publicación")
    is_available = fields.Boolean(string="Disponible", default=True)
    
    # Campo calculado para la antigüedad 
    years_since_publication = fields.Integer(
        string="Años desde publicación", 
        compute="_compute_years_since_publication",
        store=True
    )

    # Estado de disponibilidad 
    is_available = fields.Boolean(string="Disponible", default=True)

    @api.depends('published_date')
    def _compute_years_since_publication(self):
        for record in self:
            if record.published_date:
                today = date.today()
                # Calculamos la diferencia de años
                record.years_since_publication = today.year - record.published_date.year
            else:
                record.years_since_publication = 0

                