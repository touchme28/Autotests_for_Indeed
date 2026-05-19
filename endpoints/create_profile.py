import requests
from endpoints.base_endpoint import Endpoint

#Класс эндпоинта /api/profiles/ create profile
class CreateProfile(Endpoint):

    def create_profile(self, payload, token):
        self.response = requests.post(
            f'{self.BASE_URL}/api/profiles/',
            json=payload,
            headers={'Authorization': f'bearer {token}'}
        )
        self.response_json = self.response.json()

    def check_success_message(self):
        assert self.response_json['message'] == 'Profile created successfully'
        
    def check_profile_fields(self, payload):
        profile = self.response_json['profile']

        for profile_field, payload_value in payload.items():
            value = profile.get(profile_field)
            assert value == payload_value