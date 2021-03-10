from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartners(models.Model):
    _inherit = 'res.partner'

    # How to OverRide Create Method Of a Model
    @api.model
    def create(self,vals_list):
        res = super(ResPartners,self).create(vals_list)
        print("working")
        # do the custom coding here
        return res


# inheriting (merging) two fields from patient to sales application
class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        print("Hell")
        res = super(SaleOrderInherit, self).action_confirm()
        return res

    patients_name = fields.Char(string="Patient's Name")
    is_patients = fields.Boolean(string='Is Patient')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    company_type = fields.Selection(selection_add=[("Nuhaadh", "ERP Bricks"), ("Hasn", "Finsaaai")])


class HospitalPatients(models.Model):
    # model's name and desctiption
    _name = 'hospital.patients'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Patient Details, Nuhaadh'
    _rec_name = 'patients_name'  # by using this you add the name of the patient in the form view

    def print_report(self):
        return self.env.ref('hospital_nuhaadh.report_patients_cards').report_action(self)

    # @api.model
    # def test_cron_job(self):
    #     print("ABCD")

    @api.onchange('doctors_name')
    def set_doctors_gender(self):
        for rec in self:
            if rec.doctors_name:
                rec.doctors_gender = rec.doctors_name.gender

    # using this we are going get warning sign (age must be Greater than 5)
    @api.constrains('patients_age')
    def check_age(self):
        for rec in self:
            if rec.patients_age <= 5:
                raise ValidationError(_('Age must be Greater than 5'))
            elif rec.patients_age >= 200:
                raise ValidationError(_('Age must be Less than 200'))

    # this a method we compute that it is major or minor
    @api.depends('patients_age')
    def set_age_group(self):
        # by using the code below we can stop getting the error "hospital.patients(<Newld 0x7ff1503cc5c0>,).age_group
        # but you will get default text as minor in the combobox
        #   self.age_group = 'minor'
        for rec in self:
            if rec.patients_age:
                if rec.patients_age < 18:
                    rec.age_group = "minor"
                else:
                    rec.age_group = "major"

    # type = Object buttons code in the xml file
    # @api.multi - if entered this code, you will log out of server and get an error message
    def open_appointments(self):
        return {
            'name': _('Appointments'),
            'domain': [('patients_id', '=', self.id)],  # without the topple will bring all records for appointments
            'view_type': 'form',
            'res_model': 'hospital.appointments',
            'view_id': False,
            'view_mode': 'tree,form',  # after clicking the button we are getting new tree & form view
            'type': 'ir.actions.act_window',
        }

    def get_appointments_count(self):
        for rec in self:
            count = rec.env['hospital.appointments'].search_count([('patients_id', '=', rec.id)])
            rec.appointment_count = count

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s - %s' % (rec.name_seq,rec.patients_name)))
        return res

    # these are the database fields we are automatically creating using python
    name = fields.Char(string='Contact Number', track_visibility="always")
    patients_name = fields.Char(string='Name', required=True, track_visibility="always")
    patients_age = fields.Integer('Age', track_visibility="always", group_operator=False)
    patients_age2 = fields.Float('Age2')
    notes = fields.Text('Notes', track_visibility="always")
    image = fields.Binary("Image", track_visibility="always")
    name_seq = fields.Char(string='Patient ID', required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'), track_visibility="always")
    # if the selection fields is empty you will always get an error for the for that you need to use a "default value"
    # or boolean function as given below
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], default='male', string="Gender", track_visibility="always")
    age_group = fields.Selection([
        ("minor", "Minor"),
        ("major", "Major"),
    ], string="Age Group", compute="set_age_group", store=True)
    # by adding the "store=True" we can stop getting the error "hospital.patients(<Newld 0x7ff1503cc5c0>,).age_group
    # but the combobox will be empty
    address = fields.Char(string='Address')
    email_id = fields.Char(string='Email')
    appointment_count = fields.Integer(string="Appointments", compute="get_appointments_count")
    active = fields.Boolean("Active", default=True)
    doctors_name = fields.Many2one('hospital.doctors', string="Doctors")
    doctors_gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string="Doctor Gender")
    patients_name_upper = fields.Char(compute="_compute_upper_name", inverse="_inverse_upper_name")

    # Case Conversion Code
    @api.depends('patients_name')
    def _compute_upper_name(self):
        for rec in self:
            rec.patients_name_upper = rec.patients_name.upper() if rec.patients_name else False

    def _inverse_upper_name(self):
        for rec in self:
            rec.patients_name = rec.patients_name_upper.lower() if rec.patients_name_upper else False

    # code for creating "HP0001" sequence
    @api.model
    def create(self, vals):  # Re Generating the code using name_seq
        if vals.get('name_seq', _('New')) == _('New'):  # if there is a record on table continue with next number. or 1
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patients.sequence') or _('New')
        result = super(HospitalPatients, self).create(vals)
        return result
