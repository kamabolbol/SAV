from odoo import models, fields

class LLMMessage(models.Model):
    _name = 'llm.message'
    _description = 'LLM Message'
    _order = 'create_date asc'

    conversation_id = fields.Many2one('llm.conversation', string='Conversation', required=True)
    role = fields.Selection([('user', 'User'), ('assistant', 'Assistant'), ('system', 'System')], string='Role', required=True)
    content = fields.Text(string='Content', required=True)
    create_date = fields.Datetime(string='Created Date', readonly=True)
