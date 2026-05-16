import requests
from endpoints.base_endpoint import Endpoint

#Класс эндпоинта /api/auth/register
class RegisterUser(Endpoint):

    def new_user(self, payload):
        self.response = requests.post(
            f'{self.BASE_URL}/api/auth/register',
            json=payload
        )
        self.response_json = self.response.json()
    
    def check_name(self, name):
        assert self.response_json['account']['username'] == name
