import requests
from endpoints.base_endpoint import Endpoint

#Класс эндпоинта /api/profiles/{account_id} Delete profile
class DeleteProfile(Endpoint):

    def delete_profile_by_id(self, account_id, admin_token):
        self.response = requests.delete(
            f'{self.BASE_URL}/api/profiles/{account_id}',
            headers={'Authorization': f'bearer {admin_token}'}
        )
        self.response_json = self.response.json()

    def check_success_message(self):
        assert self.response_json['message'] == 'Account and profile deleted successfully'