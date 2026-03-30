from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'  # Heredamos del modelo estándar de Contactos [cite: 64]

    is_library_member = fields.Boolean(string="Es Socio de Biblioteca", default=False)
    member_code = fields.Char(string="Código de Socio", readonly=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('is_library_member') and not vals.get('member_code'):
                # Aquí llamaremos a la secuencia automática más adelante [cite: 65]
                vals['member_code'] = self.env['ir.sequence'].next_by_code('library.member.sequence')
        return super(ResPartner, self).create(vals_list)