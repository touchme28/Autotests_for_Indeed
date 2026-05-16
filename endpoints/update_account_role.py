import requests
from endpoints.base_endpoint import Endpoint

#Класс эндпоинта /api/profiles/{account_role}/role
class UpdateAccountRole(Endpoint):

    def update_role(self, account_id, role_name, admin_token):
        self.response = requests.put(
            f'{self.BASE_URL}/api/profiles/{account_id}/role',
            params={'role_name': role_name},
            headers={'Authorization': f'bearer {admin_token}'}
        )
        self.response_json = self.response.json()

    def check_success_message(self):
        assert self.response_json['message'] == 'Role updated successfully'

    def check_id(self, id):
        assert self.response_json['account_id'] == id