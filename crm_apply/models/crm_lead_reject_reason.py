# -*- coding: utf-8 -*-

from odoo import fields, models


class CrmLeadRejectReason(models.Model):
    _name = 'crm.lead.reject.reason'
    _description = 'CRM Lead Reject Reasons'

    name = fields.Char('Name', required=True, translate=True)
