import requests
from endpoints.base_endpoint import Endpoint

#Класс эндпоинта /api/profiles/me Get my profile
class GetMyProfile(Endpoint):

    def get_my_profile(self, token):
        self.response = requests.get(
            f'{self.BASE_URL}/api/profiles/me',
            headers={'Authorization': f'bearer {token}'}
        )
        self.response_json = self.response.json()

    def check_success_message(self):
        assert self.response_json['message'] == 'User profile'

    def check_profile_fields(self, payload):
        profile = self.response_json['profile']['profile']

        for profile_field, payload_value in payload.items():
            value = profile.get(profile_field)
            assert value == payload_value

        '''
        assert self.response_json['profile']['profile']['name'] == payload['name']
        assert self.response_json['profile']['profile']['surname'] == payload['surname']
        assert self.response_json['profile']['profile']['middlename'] == payload['middlename']
        assert self.response_json['profile']['profile']['birthdate'] == payload['birthdate']
        assert self.response_json['profile']['profile']['about'] == payload['about']
        assert self.response_json['profile']['profile']['links'] == payload['links']
        '''
