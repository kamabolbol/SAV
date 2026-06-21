import requests
import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class AIConnector(models.TransientModel):
    _name = 'ai.connector'
    _description = 'AI Connector to Gateway'

    prompt = fields.Text(string='Prompt', required=True)
    response = fields.Text(string='Response', readonly=True)
    model = fields.Char(string='Model', default='phi3:mini')

    def action_ask_ai(self):
        try:
            url = 'http://ai-gateway:8000/chat/'
            payload = {
                'prompt': self.prompt,
                'user_id': self.env.user.id,
                'context': {
                    'company': self.env.company.name,
                    'user': self.env.user.name
                }
            }
            resp = requests.post(url, json=payload, timeout=120)
            resp.raise_for_status()
            data = resp.json()
            self.response = data.get('response', 'Pas de réponse')
            _logger.info('AI request successful for user %s', self.env.user.id)
        except Exception as e:
            self.response = f'Erreur : {str(e)}'
            _logger.error('AI request failed: %s', e)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ai.connector',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
