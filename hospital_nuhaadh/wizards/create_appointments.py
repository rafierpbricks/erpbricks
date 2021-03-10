from odoo import models, fields, api, _


class CreateAppointments(models.TransientModel):
    _name = 'create.appointments'
    _description = 'Create New Appointment'

    patients_id = fields.Many2one('hospital.patients', string="Patient")
    appointments_date = fields.Date(string="Appointment Date")

    def print_report(self):
        data = {
            'model': 'create.appointments',
            'form' : self.read()[0]
        }
        # if data['form']['patients_id']:
        #     selected_patients = data['form']['patients_id'][0]
        #     appointments = self.env['hospital.appointments'].search([('patients_id', '=', selected_patients)])
        # else:
        #     appointments = self.env['hospital.appointments'].search([])
        # appointment_list = []
        # for app in appointments:
        #     vals = {
        #         'name_seq': app.name_seq,
        #         'notes': app.notes,
        #         'appointments_date': app.appointments_date
        #     }
        #     appointment_list.append(vals)
        # data['appointments'] = appointment_list
        return self.env.ref('hospital_nuhaadh.report_appointment').with_context(landscape=True).report_action(self,data=data)

    def delete_patients(self):
        for rec in self:
            rec.patients_id.unlink()
            print("test", rec)

    def create_appointments(self):
        # creating dictionary to pass the values
        vals = {
            'patients_id': self.patients_id.id,
            'appointments_date': self.appointments_date,
            'notes': 'Created From The Wizard/Code'
        }
        self.patients_id.message_post(body=" Appointment Created Successfully", subject="Appointment creation")
        new_appointments = self.env['hospital.appointments'].create(vals)
        context = dict(self.env.context)
        context['form_view_initial_mode'] = 'edit'
        return {'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'hospital.appointments',
                'res_id': new_appointments.id,
                'context': context
                }

    def get_data(self):
        appointments = self.env['hospital.appointments'].search([])
        appointments_count = self.env['hospital.appointments'].search_count([])
        for rec in appointments:
            print("Appointment Name", rec.name_seq)
        print("appointments", appointments)
        print("Appointments Count", appointments_count)
        return {
            "type": "ir.actions.do_nothing"
        }
