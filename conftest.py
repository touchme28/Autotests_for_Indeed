import pytest
import secrets
import string
from endpoints.register_user import RegisterUser
from endpoints.login_user import LoginUser
from endpoints.delete_profile import DeleteProfile

#Фикстуры с данными
#Данные админа - всегда одни и те же - scope = session (создается 1 раз за все тесты)
@pytest.fixture(scope='session')
def admin_token():
    admin_user = LoginUser()
    payload = {
        'username' : 'admin',
        'password' : 'admin123'
    }
    
    admin_user.login_user(payload=payload)
    return admin_user.response_json['access_token']

#Данные пользователя - есть тесты меняющие состояние - scope = function (создается для каждого теста, значение по умолчанию)
@pytest.fixture()
def user_info(admin_token):
    new_user_object = RegisterUser()
    alphabet = string.ascii_letters + string.digits
    short_id = ''.join(secrets.choice(alphabet) for _ in range(6))
    payload = {
        'username' : f'autotest_user_{short_id}',
        'email' : f'autotest_user_{short_id}@example.com',
        'password' : '123456'
    }

    new_user_object.new_user(payload=payload)
    user_id = new_user_object.response_json['account']['id']
    yield {
        'id': user_id, 
        'username': new_user_object.response_json['account']['username'], 
        'email' : new_user_object.response_json['account']['email'], 
        'password': payload['password']
    }
    delete_object = DeleteProfile()
    delete_object.delete_profile_by_id(account_id=user_id,admin_token=admin_token)

#Получение токена и информации об юзере
@pytest.fixture()
def user_token(user_info):
    default_user = LoginUser()
    payload = {
        'username' : user_info['username'],
        'password' : user_info['password']
    }

    default_user.login_user(payload=payload)
    return default_user.response_json['access_token']