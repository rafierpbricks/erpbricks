from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleInherit(WebsiteSale):
    @http.route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        '''/shop/category/<model("product.public.category"):category>''',
        '''/shop/category/<model("product.public.category"):category>/page/<int:page>'''
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        res = super(WebsiteSaleInherit, self).shop(page=0, category=None, search='', ppg=False, **post)
        print("Inherited")
        # print("res.qcontext", res.qcontext)
        # print("res.qcontext.update", res.qcontext.update({'test_vals': 'Nuhaadh Hassan'}))
        # print("res.qcontext.update", res.qcontext.update({'search': 'Hasn@'}))
        print("res.qcontext", res.qcontext)
        return res


# This is the code for the title in the hospital.appointments
class AppointmentsController(http.Controller):
    @http.route('/hospital_nuhaadh/appointments', auth='user', type='json')
    def appointment_banner(self):
        return {
            'html': """
                <div>
                    <link>
                    <center><h1><font color='red'>Nuhaadh Hasn's</font></h1></center>
                    <center>
                    <p><font color='blue'>Hospitals</p>
                        </font></div></center>"""
        }


class Hospitals(http.Controller):

    @http.route('/hospital/doctors/', type='http', auth='public', website=True)
    def hospital_doctors(self, **kw):
        print('Hellow World')
        return 'Helloo Guyssss'

    # The Below Two Http are the websites we created to add patient and appointment using website
    @http.route('/patients_webform', type='http', auth='public', website=True)
    def patients_webform(self, **kw):
        print('1', kw)
        doctor_rec = request.env['hospital.doctors'].sudo().search([])
        return http.request.render('hospital_nuhaadh.create_patients', {'doctors_rec': doctor_rec})

    @http.route('/create/webpatients', type='http', auth='public', website=True)
    def create_webpatients(self, **kw):
        print('create/webpatients')
        request.env['hospital.patients'].sudo().create(kw)
        print('2', kw)
        doctors_val = {
            'doctors_name': kw.get('patients_name'),
            'specialized': kw.get('patients_name')
        }
        request.env['hospital.doctors'].sudo().create(doctors_val)
        print('3', kw)
        return request.render('hospital_nuhaadh.patients_thanks', {})

    # list all the existing patient
    @http.route('/hospital/patients/', website=True, auth='public')
    def hospital_patients(self, **kw):
        patient = request.env['hospital.patients'].sudo().search([])
        print('Patients', patient)
        return request.render("hospital_nuhaadh.patients_page", {
            'patients': patient
        })
#
#     @http.route('/get_patients', type='json', auth='user', website=True)
#     def get_patients(self):
#         print("Yes here entered")
#         patients_rec = request.env['hospital.patients'].sudo().search([])
#         patients = []
#         for rec in patients_rec:
#             vals = {
#                 'id': rec.id,
#                 'name': rec.patients_name,
#             }
#             patients.append(vals)
#         print("Patient List--->", patients)
#         data = {'status': 200, 'response': patients, 'message': "Done All Patients Returned"}
#         print(data)
#         return data
#         # return request.render('hospital_nuhaadh.web_get_patients', {'patients_list': patients_rec})
#
