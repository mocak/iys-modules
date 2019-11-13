# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    identity_number = fields.Char('Identity Number')
    date_of_birth = fields.Date('Date of Birth')
