import requests
from endpoints.base_endpoint import Endpoint

#Класс эндпоинта /api/profiles/me Update my profile
class UpdateMyProfile(Endpoint):

    def update_my_profile(self, token, payload):
        self.response = requests.put(
            f'{self.BASE_URL}/api/profiles/me',
            json=payload,
            headers={'Authorization': f'bearer {token}'}
        )
        self.response_json = self.response.json()

    def check_success_message(self):
        assert self.response_json['message'] == 'Profile updated successfully'

    def check_updated_fields(self, payload):
        profile = self.response_json['profile']

        for profile_field, payload_value in payload.items():
            value = profile.get(profile_field)
            assert value == payload_value
