# -*- coding: utf-8 -*-

{
    'name': 'crm additional comments',
    'version': '0.1',
    'category': 'Sales/CRM',
    'sequence': 5,
    'summary': 'comments for lead',
    'description': """
    Module will add new o2m list in crm lead form, and gives an oportunity to add new comments
    and also put this comments in notes in case of need
    module is built by Soso Ninidze, for any question please contact through mail sosoninidze@gmail.com
    """,
    'website': 'kamechi.club',
    'images': [
    ],
    'depends': [
        'base_setup',
        'mail',
        'resource',
        'web',
        'sales_team',
        'crm'
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'views/crm_additional_comment_view.xml',
    ],
    'demo': [
        
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'qweb': [],
}
