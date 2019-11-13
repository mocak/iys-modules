# -*- coding: utf-8 -*-

from .. import rabbitmq

from odoo import api, fields, models


class CrmLeadDocument(models.Model):
    _name = 'crm.lead.document'
    _description = 'Lead Documents'

    name = fields.Char('File Name')
    lead_id = fields.Many2one('crm.lead', 'Lead')
    file = fields.Binary('File', attachment=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
    ], 'State', default='draft', required=True)

    @api.multi
    def confirm(self):
        """Confirms document and notifies backend if all documents has approved"""
        self.write({'state': 'confirmed'})

        # notify backend that the document was approved
        rabbitmq.client.publish({
            'document_ids': self.ids,
            'document_names': self.mapped('name'),
        })

        states = self.mapped('lead_id').mapped('document_state')
        if set(states) == {'confirmed'}:
            # notify backend that the lead was approved
            rabbitmq.client.publish({
                'reference': self.lead_id.internal_reference,
                'lead_ids': self.mapped('lead_id').mapped('id'),
            })

        return {'type': 'ir.actions.client', 'tag': 'reload'}
