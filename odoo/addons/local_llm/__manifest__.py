{
    'name': 'Local LLM Connector',
    'version': '1.0',
    'category': 'AI',
    'summary': 'Connect Odoo to AI Gateway',
    'depends': ['base', 'web', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/ai_connector_views.xml',
        'views/llm_menu_views.xml',
    ],
    'installable': True,
    'application': True,   # ← modifié ici
}