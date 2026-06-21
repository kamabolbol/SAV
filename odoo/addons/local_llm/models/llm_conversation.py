from odoo import models, fields, api

class LLMConversation(models.Model):
    _name = 'llm.conversation'
    _description = 'LLM Conversation'
    _order = 'write_date desc'

    name = fields.Char(string='Name', required=True)
    user_id = fields.Many2one('res.users', string='User', required=True)
    config_id = fields.Many2one('llm.config', string='Configuration', required=True)
    message_ids = fields.One2many('llm.message', 'conversation_id', string='Messages')
    message_count = fields.Integer(string='Message Count', compute='_compute_message_count')
    active = fields.Boolean(string='Active', default=True)
    last_message_date = fields.Datetime(string='Last Message Date')

    @api.depends('message_ids')
    def _compute_message_count(self):
        for rec in self:
            rec.message_count = len(rec.message_ids)
