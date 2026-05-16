import requests
from endpoints.base_endpoint import Endpoint

#Класс эндпоинта /api/profiles/{account_id} Update profile
class UpdateProfile(Endpoint):

    def update_profile(self, account_id, payload, token):
        self.response = requests.put(
            f'{self.BASE_URL}/api/profiles/{account_id}',
            json=payload,
            headers={'Authorization': f'bearer {token}'}
        )
        self.response_json = self.response.json()

    def check_success_message(self):
        assert self.response_json['message'] == 'Profile updated successfully'

    def check_updated_fields(self, payload):
        assert self.response_json['profile']['name'] == payload['name']
        assert self.response_json['profile']['surname'] == payload['surname']
        assert self.response_json['profile']['middlename'] == payload['middlename']
        assert self.response_json['profile']['birthdate'] == payload['birthdate']
        assert self.response_json['profile']['about'] == payload['about']
        assert self.response_json['profile']['links'] == payload['links']