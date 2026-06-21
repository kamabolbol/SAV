from odoo import models, fields, api

class LLMConfig(models.Model):
    _name = 'llm.config'
    _description = 'LLM Configuration'

    name = fields.Char(string='Name', required=True)
    api_url = fields.Char(string='API URL', required=True)
    model_name = fields.Char(string='Model Name', required=True)
    active = fields.Boolean(string='Active', default=True)
    is_default = fields.Boolean(string='Default', default=False)
    provider = fields.Char(string='Provider', default='ollama')
    temperature = fields.Float(string='Temperature', default=0.7)
    max_tokens = fields.Integer(string='Max Tokens', default=512)
    system_prompt = fields.Text(string='System Prompt')
    request_timeout = fields.Integer(string='Request Timeout (ms)', default=60000)
    max_history_messages = fields.Integer(string='Max History Messages', default=20)
