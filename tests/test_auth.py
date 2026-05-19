import pytest
import secrets
import string
from endpoints.register_user import RegisterUser
from endpoints.login_user import LoginUser
from endpoints.verify_user import VerifyUser
from endpoints.change_password import ChangePassword
from endpoints.delete_profile import DeleteProfile

@pytest.mark.auth
class TestAuthentication:
    #проверка регистрации
    def test_register_new_user_success(self, admin_token):
        new_user_object = RegisterUser()

        alphabet = string.ascii_letters + string.digits
        short_id = ''.join(secrets.choice(alphabet) for _ in range(6))
        payload = {
            'username' : f'autotest_user_{short_id}',
            'email' : f'autotest_user_{short_id}@example.com',
            'password' : '123456'
        }

        new_user_object.new_user(payload=payload)
        new_user_object.check_response_is_200()
        new_user_object.check_name(payload['username'])

        delete_object = DeleteProfile()
        delete_object.delete_profile_by_id(
            account_id=new_user_object.response_json['account']['id'],
            admin_token=admin_token
        )

    @pytest.mark.parametrize('duplicate_field, value', [
        ('username', 'test@example.com'),
        ('email', 'test_user')
    ])
    #проверка регистрации с уже существующим полем (именем или почтой) с помощью параметризации
    def test_register_duplicate_fields_fails(self, user_info, duplicate_field, value):
        new_user_object = RegisterUser()

        if duplicate_field == 'username':
            payload = {
                'username' : user_info['username'],
                'email' : value,
                'password' : '123456'
            }
        else:
            payload = {
                'username' : value,
                'email' : user_info['email'],
                'password' : '123456'
            }

        new_user_object.new_user(payload=payload)
        new_user_object.check_response_is_400()

    #проверка на отсутсвие обязательных полей
    def test_register_missing_fields(self):
        new_user_object = RegisterUser()

        payload = {
            'username' : 'user_without_email',
            'password' : '123456'
        }

        new_user_object.new_user(payload=payload)
        new_user_object.check_response_is_422()

    #проверка входа с валидными данными
    def test_login_valid_data(self, user_info):
        default_user = LoginUser()
        payload = {
            'username' : user_info['username'],
            'password' : user_info['password']
        }
        default_user.login_user(payload)
        default_user.check_response_is_200()
        default_user.check_name(payload['username'])
        default_user.check_token()

    #проверка входа с невалидными данными
    def test_login_invalid_data(self, user_info):
        default_user = LoginUser()
        payload = {
            'username' : user_info['username'],
            'password' : 'wrong password'
        }
        default_user.login_user(payload)
        default_user.check_response_is_401()

    #проверка валидного токена
    def test_verify_valid_token(self, user_token):
        verify_default_user = VerifyUser()
        verify_default_user.verify_user(user_token)
        verify_default_user.check_response_is_200()
        verify_default_user.check_success_message()
        verify_default_user.check_id_username_email()

    #проверка невалидного токена
    def test_verify_invalid_token(self):
        verify_default_user = VerifyUser()
        verify_default_user.verify_user('invalid_token')
        verify_default_user.check_response_is_401()

    #проверка успешной смены пароля
    def test_change_password_success(self, user_info, user_token):
        change_password_object = ChangePassword()
        payload = {
            'old_password' : user_info['password'],
            'new_password' : '123'
        }
        change_password_object.change_password(payload, user_token)
        change_password_object.check_response_is_200()
        change_password_object.check_success_message()
    
    #проверка ошибки, если старый пароль не верный
    def test_change_password_fails(self, user_token):
        change_password_object = ChangePassword()
        payload = {
            'old_password' : 'wrong old password',
            'new_password' : '123'
        }
        change_password_object.change_password(payload, user_token)
        change_password_object.check_response_is_400()
    
    #проверка ошибки, если запрос был сделан с помощью невалидного токена
    def test_change_password_unauthorized(self):
        change_password_object = ChangePassword()
        payload = {
            'old_password' : 'test',
            'new_password' : 'test'
        }
        token = 'invalid_token'
        change_password_object.change_password(payload, token)
        change_password_object.check_response_is_401()