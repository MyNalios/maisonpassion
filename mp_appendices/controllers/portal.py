# -*- coding: utf-8 -*-
from odoo import fields, http, _
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.http import request


class CustomerPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        """ compute document count for portal home """
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        partner = request.env.user.partner_id

        document_count = request.env['sale.technical.document'].search_count([('partner_ids', '=', partner.id)])

        values.update({
            'document_count': document_count,
        })
        return values

    @http.route(['/my/documents', '/my/documents/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_documents(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id

        Document = request.env['sale.technical.document']

        domain = ([('partner_ids', '=', partner.id)])

        searchbar_sortings = {
            'name': {'label': _('Document Name'), 'order': 'name'},
        }

        # default sortby order
        if not sortby:
            sortby = 'name'
        sort_order = searchbar_sortings[sortby]['order']

        archive_groups = self._get_archive_groups('sale.technical.document', domain)

        # count for pager
        document_count = Document.search_count(domain)
        # make pager
        pager = portal_pager(
            url="/my/quotes",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=document_count,
            page=page,
            step=self._items_per_page
        )
        # search the count to display, according to the pager data
        documents = Document.search(domain, order=sort_order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_documents_history'] = documents.ids[:100]

        values.update({
            'date': date_begin,
            'documents': documents.sudo(),
            'page_name': 'document',
            'pager': pager,
            'archive_groups': archive_groups,
            'default_url': '/my/documents',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return request.render("mp_appendices.portal_my_documents", values)
