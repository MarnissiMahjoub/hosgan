# -*- coding: utf-8 -*-
{
    'name': "ms_crm_hosgan_intervention",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "MS Solution ERP / Mahjoub",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','crm'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views_crm.xml',
        'views/view_bilan.xml',
        'views/intervention.xml',
        'views/views_ordonnance_medicale_wizard.xml',
        'views/views_ordonnance_wizard.xml',
        'views/views_bilan_wizard.xml',
        'views/views_ordonnance.xml',
        'views/templates_2.xml',
        'views/templates_3.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}

