# -*- coding: utf-8 -*-

from .. import rabbitmq

from odoo import api, fields, models


class CrmLeadRejectWizard(models.TransientModel):
    _name = 'crm.lead.reject.wizard'
    _description = 'CRM Lead Reject Wizard'

    def _default_lead_id(self):
        return self.env.context.get('active_id')

    lead_id = fields.Many2one('crm.lead', 'Lead', default=_default_lead_id)
    reject_reason_id = fields.Many2one('crm.lead.reject.reason',
                                       'Reject Reason')

    @api.multi
    def reject(self):
        self.ensure_one()
        self.lead_id.sudo().write({
            'reject_reason_id': self.reject_reason_id.id,
            'state': 'rejected',
        })

        # notify backend
        rabbitmq.client.publish({
            'message': 'Lead Rejected',
            'reason': self.reject_reason_id.name,
            'lead_id': self.lead_id.id,
        })
