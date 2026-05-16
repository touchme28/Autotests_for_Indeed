import requests
from endpoints.base_endpoint import Endpoint

#Класс эндпоинта /api/profiles/ list profiles
class ListProfiles(Endpoint):

    def list_profiles(self, token: str, limit: int = 100, offset: int = 0):
        params = {
            'limit' : limit,
            'offset' : offset
        }
        self.response = requests.get(
            f'{self.BASE_URL}/api/profiles/',
            headers={'Authorization': f'bearer {token}'},
            params=params
        )
        self.response_json = self.response.json()

    def check_list_contains_user(self, user_id):
        ids = [user_in_list.get('id') for user_in_list in self.response_json['profiles']]
        assert user_id in ids

    def check_list_not_empty(self):
        assert self.response_json['count'] != 0

    def check_list_contains_only_user(self):
        assert self.response_json['count'] == 1

    def check_list_limit(self, limit):
        assert self.response_json['count'] <= limit