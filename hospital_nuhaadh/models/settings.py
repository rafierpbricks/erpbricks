# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from ast import literal_eval


class HospitalSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    notes = fields.Char(string='Default Note')
    module_crm = fields.Boolean(string='CRM')
    product_ids = fields.Many2many('product.product', string='Medicine')

    def set_values(self):
        res = super(HospitalSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('hospital_nuhaadh.notes', self.notes)
        print('test', self.product_ids.ids)
        self.env['ir.config_parameter'].set_param('hospital_nuhaadh.product_ids', self.product_ids.ids)
        return res

    @api.model
    def get_values(self):
        res = super(HospitalSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        notes = ICPSudo.get_param('hospital_nuhaadh.notes')
        product_ids = self.env['ir.config_parameter'].sudo().get_param('hospital_nuhaadh.product_ids')
        print("product ids", product_ids)
        if product_ids:
            res.update(
                notes=notes,
                product_ids=[(6, 0, literal_eval(product_ids))],
            )
        return res
