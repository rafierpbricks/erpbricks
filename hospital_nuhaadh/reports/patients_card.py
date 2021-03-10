from odoo import api, models, _


class PatientsCardReport(models.AbstractModel):
    _name = 'report.hospital_nuhaadh.report_patients'
    _description = 'Patients Card Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['hospital.patients'].browse(docids[0])
        appointments = self.env['hospital.appointments'].search([('patients_id', '=', docids[0])])
        appointments_list = []
        print("docids ", docids)
        for app in appointments:
            vals = {
                'name_seq': app.name_seq,
                'notes': app.notes,
                'appointments_date': app.appointments_date
            }
            appointments_list.append(vals)
        print("appointments ", appointments)
        print("appointments_list", appointments_list)
        return {
            'doc_model': 'hospital.patients',
            'data' : data,
            'docs': docs,
            'appointments_list': appointments_list,
        }
