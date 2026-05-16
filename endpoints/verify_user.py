import requests
from endpoints.base_endpoint import Endpoint

#Класс эндпоинта /api/auth/verify
class VerifyUser(Endpoint):

    def verify_user(self, token):
        self.response = requests.post(
            f'{self.BASE_URL}/api/auth/verify',
            headers={'Authorization': f'bearer {token}'}
        )
        self.response_json = self.response.json()
    
    def check_success_message(self):
        assert self.response_json['message'] == 'Token is valid'

    def check_id_username_email(self):
        assert 'id' in self.response_json['user']
        assert 'username' in self.response_json['user']
        assert 'email' in self.response_json['user']