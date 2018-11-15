{
    'name': 'Orden de Trabajo',
    'version': '1.0',
    'summary': 'Personalizacion del modulo CRM',
    'description': '',
    'category': 'Personalizacion',
    'author': 'xmarts',
    'website': 'www.xmarts.com',
    'depends': ['base', 'contacts','hr','fleet','sale','crm','helpdesk','hr_expense'],
    'data': ['views/view.xml',
             'reports/deliver_split.xml',
            ],

    'installable': True,
    'aplication': True,
    'auto_install': False,
}


