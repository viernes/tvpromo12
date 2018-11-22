# -*- coding: utf-8 -*-
from odoo import http

# class XmartsPartnerAttendances(http.Controller):
#     @http.route('/xmarts_partner_attendances/xmarts_partner_attendances/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/xmarts_partner_attendances/xmarts_partner_attendances/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('xmarts_partner_attendances.listing', {
#             'root': '/xmarts_partner_attendances/xmarts_partner_attendances',
#             'objects': http.request.env['xmarts_partner_attendances.xmarts_partner_attendances'].search([]),
#         })

#     @http.route('/xmarts_partner_attendances/xmarts_partner_attendances/objects/<model("xmarts_partner_attendances.xmarts_partner_attendances"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('xmarts_partner_attendances.object', {
#             'object': obj
#         })