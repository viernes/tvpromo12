{
    'name': 'Orden de Trabajo',
    'version': '1.0',
    'summary': 'Personalizacion del modulo CRM',
    'description': '',
    'category': 'Personalizacion',
    'author': 'xmarts',
    'website': 'www.xmarts.com',
    'depends': ['base', 'hr_attendance','contacts','hr','fleet','sale','crm','helpdesk','hr_expense','stock','project','hr_holidays','sale_management','timesheet_grid','account'],
    'data': ['views/view.xml',
             'reports/deliver_split.xml',
            ],

    'installable': True,
    'aplication': True,
    'auto_install': False,
}


