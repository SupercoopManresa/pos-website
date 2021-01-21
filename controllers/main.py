# -*- coding: utf-8 -*-
#################################################################################
# Author : Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>;
#################################################################################
from odoo.exceptions import AccessError
import logging
_logger = logging.getLogger(__name__)
from odoo.http import Controller, request, route
from odoo import http, _, fields, models, api
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager


class CustomerPortalInherit(CustomerPortal):

    @route(['/my', '/my/home'], type='http', auth="user", website=True)
    def home(self, **kw):
        result = super(CustomerPortalInherit, self).home(**kw)
        user = request.env['res.users'].sudo().browse(request.session.uid)
        PosOrder = request.env['pos.order'].sudo()
        domain = [
            ('partner_id', '=', user.partner_id.id),
            ('state', 'in', ['invoiced', 'done','paid'])
        ]

        order_count = PosOrder.search_count(domain)
        result.qcontext.update({
            'pos_order_count':order_count
            })
        return result

    @route(['/my/pos_orders', '/my/pos_orders/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_pos_orders(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.sudo().partner_id
        PosOrder = request.env['pos.order'].sudo()
        domain = [
            ('partner_id', '=', partner.id),
            ('state', 'in', ['invoiced', 'done', 'paid'])
        ]

        searchbar_sortings = {
            'date': {'label': _('Order Date'), 'order': 'date_order desc'},
            'name': {'label': _('Reference'), 'order': 'name'},
            'stage': {'label': _('Stage'), 'order': 'state'},
        }
        # default sortby order
        if not sortby:
            sortby = 'date'
        sort_order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        order_count = PosOrder.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/pos_orders",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=order_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        orders = PosOrder.search(domain, order=sort_order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_pos_orders_history'] = orders.ids[:100]

        values.update({
            'date': date_begin,
            'orders': orders.sudo(),
            'page_name': 'pos_order',
            'pager': pager,
            'default_url': '/my/orders',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return request.render("pos_website.portal_my_pos_orders", values)




    @http.route(['/my/pos_orders/<int:order>'], type='http', auth="user", website=True)
    def pos_orders_followup(self, order=None, **kw):
        order = request.env['pos.order'].sudo().browse([order])
        try:
            order.check_access_rights('read')
            order.check_access_rule('read')
        except AccessError:
            return request.render("website.403")

        order_invoice_id = order.sudo().invoice_id
        return request.render("pos_website.pos_orders_followup", {
            'order': order.sudo(),
            'page_name': 'pos_order',
            'order_invoice_lines': order.invoice_id.invoice_line_ids,
            'invoices':[order_invoice_id],
            'o':order_invoice_id
        })



class PosOrder(models.Model):
    _inherit = "pos.order"
    @api.model
    def pos_website_demo(self):
        partner = self.env['res.partner'].browse(3)
        if partner and partner.id:
            partner.customer = True
            orders = self.search([('state','!=','invoiced')])
            for order in orders:
                order.partner_id = partner

        