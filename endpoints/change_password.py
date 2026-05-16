import requests
from endpoints.base_endpoint import Endpoint

#Класс эндпоинта /api/auth/change-password
class ChangePassword(Endpoint):

    def change_password(self, payload, token):
        self.response = requests.post(
            f'{self.BASE_URL}/api/auth/change-password',
            json=payload,
            headers={'Authorization': f'bearer {token}'}
        )
        self.response_json = self.response.json()

    def check_success_message(self):
        assert self.response_json['message'] == 'Password changed successfully'