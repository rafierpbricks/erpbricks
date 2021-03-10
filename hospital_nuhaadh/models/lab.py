from odoo import models, fields


class HospitalLab(models.Model):
    _name = 'hospital.labs'
    _description = 'Hospital Laboratory, Nuhaadh'

    name = fields.Char(string="Name", required=True)
    user_id = fields.Many2one('res.users', string='Responsible')
