{
    'name': 'TVP',
    'version': '1.0',
    'summary': 'Personalizacion de campos',
    'description': 'Personalizacion en diferentes modulos como: Fleet, Sales, Helpdesk, Stock al igual que reporte "Delivery Split"',
    'category': 'Personalizacion',
    'author': 'Xmarts',
    'website': 'www.xmarts.com',
    'depends': ['base', 'hr_attendance','contacts','hr','fleet','sale','helpdesk','hr_expense','stock','project','hr_holidays','sale_management','timesheet_grid','account'],
    'data': ['views/view.xml',
             'reports/deliver_split.xml'],

    'installable': True,
    'aplication': True,
    'auto_install': False,
}


