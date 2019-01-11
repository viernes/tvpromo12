# -*- coding: utf-8 -*-
from odoo import http

# class RemOfficerLeave(http.Controller):
#     @http.route('/rem_officer_leave/rem_officer_leave/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rem_officer_leave/rem_officer_leave/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rem_officer_leave.listing', {
#             'root': '/rem_officer_leave/rem_officer_leave',
#             'objects': http.request.env['rem_officer_leave.rem_officer_leave'].search([]),
#         })

#     @http.route('/rem_officer_leave/rem_officer_leave/objects/<model("rem_officer_leave.rem_officer_leave"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rem_officer_leave.object', {
#             'object': obj
#         })