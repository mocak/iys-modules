# -*- coding: utf-8 -*-
{
    'name': "Crm Apply",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Murat Ocak <mehmetmuratocak@gmail.com>",
    'website': "http://iys.org.tr",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['crm'],

    # always loaded
    'data': [
        # security
        'security/crm_security.xml',
        'security/ir.model.access.csv',
        # views
        'views/crm_lead_views.xml',
        'views/crm_lead_document_views.xml',
        'views/res_partner_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/res_users.xml',
    ],
}