from odoo import models, fields, api, _
import pytz
from odoo.exceptions import ValidationError


class HospitalAppointments(models.Model):
    # model's name and desctiption
    _name = 'hospital.appointments'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'appointments, Nuhaadh'
    _rec_name = 'patients_id'
    _order = 'id desc'

    # _order = 'appointments_date desc'
    def test_recordset(self):
        for rec in self:
            print("Odoo ORM")
            partners = self.env['res.partner'].search([])
            print("Mapped partners Name...", partners.mapped('name'))
            print("Mapped partners Phone...", partners.mapped('phone'))
            print("Mapped partners Email...", partners.mapped('email'))
            print("Sorted partners Email...", partners.sorted(lambda o: o.create_date))

    def action_notify(self):
        for rec in self:
            rec.doctors_name.user_id.notify_success(message="My Success message")

    # notify_danger = red | notify_warning = yellow | notify_info = blue | notify_default = grey | notify_success = green

    def time_lines(self):
        for rec in self:
            if not rec.appointments_datetime:
                print("Appointments Datetime is Empty")
            else:
                print("Time in UTC", rec.appointments_datetime)
                user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
                print("user_tz", user_tz)
                date_today = pytz.utc.localize(rec.appointments_datetime).astimezone(user_tz)
                print('Time in Local timezone', date_today)

    def delete_lines(self):
        for rec in self:
            rec.appointments_lines = [(5, 0, 0)]

    def action_confirm(self):
        for rec in self:
            rec.state = "confirm"
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Appointment Confirmed... Thank You',
                    'type': 'rainbow_man',
                }
            }

    def action_done(self):
        for rec in self:
            rec.state = "done"
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Appointment Done... Thank You',
                    'type': 'rainbow_man',
                }
            }

    def action_cancel(self):
        for rec in self:
            rec.state = "draft"
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Appointment Reset... Thank You',
                    'type': 'rainbow_man',
                }
            }

    def _get_default_note(self):
        return
        # return "\n " \
        #        "\n" \
        #        "\n  ======================================" \
        #        "\n Thank you for using Nuhaadh's Hospital Services"

    def _get_default_name(self):
        return 3

    # code for creating "HP0001" sequence
    @api.model
    def create(self, vals):  # Re Generating the code using name_seq
        if vals.get('name_seq', _('New')) == _('New'):  # if there is a record on table continue with next number. or 1
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.appointments.sequence') or _('New')
        result = super(HospitalAppointments, self).create(vals)
        return result

    def write(self, vals):
        res = super(HospitalAppointments, self).write(vals)
        print(vals)
        return res

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for rec in self:
            return {'domain': {'order_id': [('partner_id', '=', rec.partner_id.id)]}}

    @api.model
    def default_get(self, fields):
        res = super(HospitalAppointments, self).default_get(fields)
        res['patients_id'] = 3
        return res

    name_seq = fields.Char(string='Appointment ID', required=True, copy=False, readonly=True, index=True,
                           default=lambda self: _('New'))
    patients_id = fields.Many2one('hospital.patients', string='Patients', required=True, default=_get_default_name)
    patients_age = fields.Integer(string='Age', related='patients_id.patients_age')  # get age from patient field
    notes = fields.Text(string="Registration Note", default=_get_default_note)
    doctor_notes = fields.Text(string="Note")
    appointments_lines = fields.One2many('hospital.appointments.lines', 'appointments_id', string='Appointment Lines')
    pharmacy_notes = fields.Text(string="Note")
    appointments_date = fields.Date(string='Date')
    appointments_date_end = fields.Date(string='Date End')
    appointments_datetime = fields.Datetime(string='Date Time')
    partner_id = fields.Many2one(comodel_name="res.partner", string="Customer")
    order_id = fields.Many2one(comodel_name="sale.order", string="Sale Order")
    name = patients_id
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, default='draft')
    doctors_name = fields.Many2one('hospital.doctors', string='Doctor')
    # doctor_ids = fields.Many2many('hospital.doctors', 'hospital_patient_rel', 'appointment_id', 'doctor_id_rec',
    #                               string='Doctors')
    total_amount = fields.Float(string="Total Amount")


class HospitalAppointmentsLines(models.Model):
    _name = 'hospital.appointments.lines'
    _description = 'Appointment Lines'

    products_id = fields.Many2one('product.product', string='Medicine')
    products_qty = fields.Integer(string='Quantity')
    # sequence = fields.Integer(string="Sequence")
    appointments_id = fields.Many2one('hospital.appointments', string='Appointment ID')
    sequence = fields.Integer(string="Sequence")
