import requests
from endpoints.base_endpoint import Endpoint

#Класс эндпоинта /api/profiles/{account_id} Get profile
class GetProfile(Endpoint):

    def get_profile(self, account_id, token):
        self.response = requests.get(
            f'{self.BASE_URL}/api/profiles/{account_id}',
            headers={'Authorization': f'Bearer {token}'}
        )
        self.response_json = self.response.json()

    def check_success_message(self):
        assert self.response_json['message'] == 'Profile retrieved successfully'