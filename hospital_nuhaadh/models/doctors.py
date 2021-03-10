from odoo import models, fields, api, _, exceptions
from odoo.exceptions import ValidationError


class HospitalDoctors(models.Model):
    # model's name and desctiption
    _name = 'hospital.doctors'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Doctors Details, Nuhaadh'
    _rec_name = 'doctors_name'  # by using this you add the name of the patient in the form view

    @api.model
    def create(self, vals):  # Re Generating the code using name_seq
        if vals.get('name_seq', _('New')) == _('New'):  # if there is a record on table continue with next number. or 1
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.doctors.sequence') or _('New')
        result = super(HospitalDoctors, self).create(vals)
        return result

    contact_number = fields.Char(string='Contact Number', track_visibility="always")
    doctors_name = fields.Char(string='Name', required=True, track_visibility="always")
    doctors_age = fields.Integer('Age', track_visibility="always")
    image = fields.Binary("Image", track_visibility="always")
    name_seq = fields.Char(string='Doctors ID', required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'), track_visibility="always")
    # if the selection fields is empty you will always get an error for the for that you need to use a "default value"
    # or boolean function as given below
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], default='male', string="Gender", track_visibility="always")
    address = fields.Char(string='Address')
    active = fields.Boolean("Active", default=True)
    specialized = fields.Char('Specialized In', required=True)
    user_id = fields.Many2one('res.users', string='Related User')
    # name_seq = fields.Many2one('hospital.patient', string='Related Patient')
    # related_patient_id = fields.Many2one('hospital.patient', string='Related Patient ID')

    # appointment_ids = fields.Many2many('hospital.appointments', 'hospital_patients_rel',
    #                                    'doctors_name_rec', 'name_seq', string='Appointments')

    def notify_success(self):
        for rec in self:
            rec.env.user.notify_success(message="My Success message")

    def notify_danger(self):
        for rec in self:
            rec.env.user.notify_danger(message='My danger message')

    def notify_warning(self):
        for rec in self:
            rec.env.user.notify_warning(message='My warning message')

    def notify_info(self):
        for rec in self:
            rec.env.user.notify_info(message='My information message')

    def notify_default(self):
        for rec in self:
            rec.env.user.notify_default(message='My default message')