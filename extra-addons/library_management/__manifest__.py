{
    'name': 'Library Management', # Nombre oficial [cite: 59]
    'version': '1.0',
    'author': 'Ismael Garcia',
    'category': 'Services/Library',
    'summary': 'Gestión de socios, libros y préstamos [cite: 59]',
    'depends': [
        'base', 
        'contacts',     
        'product',      
        'point_of_sale', 
        'website',      
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/book_views.xml',
        'views/partner_views.xml',
        'views/loan_views.xml' 
    ],
    'installable': True,
    'application': True, 
    'license': 'LGPL-3',
}