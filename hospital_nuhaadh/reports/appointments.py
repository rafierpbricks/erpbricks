from odoo import api, models, _


class AppointmentsReport(models.AbstractModel):
    _name = 'report.hospital_nuhaadh.appointment_report'
    _description = 'Appointment Report'

    @api.model
    # you can also use the "create_appointments" print method by uncommenting the lines in it and commenting this
    # appointment module from init.py
    def _get_report_values(self, docids, data=None):
        if data['form']['patients_id']:
            appointments = self.env['hospital.appointments'].search([('patients_id', '=', data['form']['patients_id'][0])])
        else:
            appointments = self.env['hospital.appointments'].search([])
        # appointment_list = []
        # for app in appointments:
        #     vals = {
        #         'name': app.name,
        #         'notes': app.notes,
        #         'appointment_date': app.appointment_date
        #     }
        #     appointment_list.append(vals)
        return {
            'doc_model': 'hospital.patients',
            'appointments': appointments,
        }
