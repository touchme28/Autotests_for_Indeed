import requests
from endpoints.base_endpoint import Endpoint

#Класс эндпоинта /api/auth/login
class LoginUser(Endpoint):

    def login_user(self, payload):
        self.response = requests.post(
            f'{self.BASE_URL}/api/auth/login',
            json=payload
        )
        self.response_json = self.response.json()
    
    def check_name(self, name):
        assert self.response_json['user']['username'] == name

    def check_token(self):
        assert self.response_json['token_type'] == 'bearer'
        assert 'access_token' in self.response_json
