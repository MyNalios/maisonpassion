# -*- coding: utf-8 -*-
# from odoo import http


# class MpCustos(http.Controller):
#     @http.route('/mp_custos/mp_custos', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mp_custos/mp_custos/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mp_custos.listing', {
#             'root': '/mp_custos/mp_custos',
#             'objects': http.request.env['mp_custos.mp_custos'].search([]),
#         })

#     @http.route('/mp_custos/mp_custos/objects/<model("mp_custos.mp_custos"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mp_custos.object', {
#             'object': obj
#         })
