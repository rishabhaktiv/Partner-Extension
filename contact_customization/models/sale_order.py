# -*- coding: utf-8 -*-

from odoo import models, fields

class ResPartnerExtended(models.Model):
    _name = "sale.order.extended"
    _inherit = "sale.order"

    transaction_ids = fields.Many2many(
        comodel_name='payment.transaction',
        relation='sale_order_transaction_extended_rel', column1='sale_order_id_extended',
        column2='transaction_id_extended',
        string="Transactions",
        copy=False, readonly=True)

    tag_ids = fields.Many2many(
        comodel_name='crm.tag',
        relation='sale_order_tag_extended_rel', column1='order_id_extended', column2='tag_id_extended',
        string="Tags")