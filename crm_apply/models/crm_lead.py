# -*- coding: utf-8 -*-

from .. import rabbitmq

from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'
    _order = 'is_high_priority DESC, create_date DESC'

    internal_reference = fields.Char('Reference')

    # Partner related fields
    partner_logo = fields.Binary("Logo",
                                 related='partner_id.image_small')
    vat = fields.Char(related='partner_id.vat')
    vat_state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
    ], default='draft')

    invoice_id = fields.Many2one('res.partner', 'Invoice',
                                 compute='_compute_invoice_id', store=True)
    invoice_address = fields.Char('Invoice Address',
                                  related='invoice_id.street')

    contact_id = fields.Many2one('res.partner', 'Contact',
                                 compute='_compute_contact_id', store=True)
    contact_identity_number = fields.Char('Identity Number',
                                          related='contact_id.identity_number')
    contact_email = fields.Char('Email', related='contact_id.email')
    contact_mobile = fields.Char('Gsm', related='contact_id.mobile')
    contact_date_of_birth = fields.Date('Date of Birth',
                                        related='contact_id.date_of_birth')

    # Segment and priority
    segment = fields.Selection([
        ('large', 'Large'),
        ('medium', 'Medium'),
        ('small', 'Small'),
    ], 'Segment')
    is_high_priority = fields.Boolean('Is high priority?', default=False)

    # Documents
    document_ids = fields.One2many('crm.lead.document', 'lead_id', 'Documents')
    document_state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
    ], 'Document State', compute='_compute_document_state', stored=True)

    @api.depends('document_ids.state')
    def _compute_document_state(self):
        for lead in self:
            state = set(self.document_ids.mapped('state'))
            lead.document_state = 'confirmed' if state == {'confirmed'} else 'draft'

    @api.depends('partner_id.child_ids')
    def _compute_contact_id(self):
        for lead in self:
            contacts = lead.partner_id.child_ids.filtered(lambda r: r.type == 'contact')
            lead.contact_id = contacts[0] if contacts else None

    @api.depends('partner_id.child_ids')
    def _compute_invoice_id(self):
        for lead in self:
            invoices = lead.partner_id.child_ids.filtered(lambda r: r.type == 'invoice')
            lead.invoice_id = invoices[0] if invoices else None

    @api.multi
    def _publish_vat_approval(self, state):
        rabbitmq.client.publish({
            'vat_ids': self.ids,
            'vats': self.mapped('vat'),
            'state': state,
        })

    # CRUD operations

    @api.multi
    def write(self, values):
        """Enables assign operation only for back-office manager"""
        is_bo_manager = self.env.user.has_group(
            'crm_apply.crm_group_back_office_manager')
        is_acc_manager = self.env.user.has_group(
            'crm_apply.crm_group_account_manager')

        if ([*values.keys()] == ['user_id']
                and self.internal_reference
                and (is_bo_manager
                     or (is_acc_manager
                         and values.get('user_id') == self.env.user.id))):
            return super(CrmLead, self.sudo()).write(values)

        return super(CrmLead, self).write(values)

    # Actions

    @api.multi
    def confirm_vat(self):
        """Confirms VAT """
        self.sudo().write({'vat_state': 'confirmed'})
        self._publish_vat_approval('confirmed')

    @api.multi
    def reject_vat(self):
        """Rejects VAT """
        self.sudo().write({'vat_state': 'rejected'})
        self._publish_vat_approval('rejected')

    @api.model
    @api.returns('self')
    def register(self, values):
        """Creates Lead from given values"""

        # create partner
        partner = self.env['res.partner'].create({
            'name': values.get('company_name'),
            'image': values.get('logo'),
            'vat': values.get('vat'),
            'child_ids': [
                (0, 0, {
                    'type': 'invoice',
                    'name': '%s Invoice Address' % values.get('company_name'),
                    'street': values.get('invoice_address')}),
                (0, 0, {
                    'type': 'contact',
                    'name': '%s %s' % (values.get('contact_name'),
                                       values.get('contact_surname')),
                    'identity_number': values.get('contact_tckn'),
                    'date_of_birth': values.get('contact_dob'),
                    'mobile': values.get('contact_gsm'),
                    'email': values.get('contact_email'),
                })
            ],
        })

        document_ids = []
        for doc in values.get('documents'):
            document_ids.append((0, 0, {'name': doc.get('name'),
                                        'file': doc.get('file')}))
        # create lead
        return self.env['crm.lead'].create({
            'type': 'opportunity',
            'name': '%s %s' % (values.get('company_name'),
                               values.get('reference')),
            'internal_reference': values.get('reference'),
            'partner_id': partner.id,
            'segment': values.get('segment'),
            'is_high_priority': values.get('is_high_priority'),
            'email_from': values.get('contact_email'),
            'contact_mobile': values.get('contact_gsm'),
            'document_ids': document_ids,
            'user_id': None
        })
