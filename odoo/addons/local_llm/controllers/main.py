from odoo import http
from odoo.http import request

class AIController(http.Controller):

    @http.route('/ai/chat', type='json', auth='user')
    def chat(self, prompt, **kwargs):
        connector = request.env['ai.connector'].create({'prompt': prompt})
        connector.action_ask_ai()
        return {'response': connector.response}
