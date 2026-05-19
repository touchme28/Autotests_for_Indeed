import pytest
import secrets
import string
from endpoints.register_user import RegisterUser
from endpoints.login_user import LoginUser
from endpoints.create_profile import CreateProfile
from endpoints.get_list_profiles import ListProfiles
from endpoints.get_my_profile import GetMyProfile
from endpoints.update_my_profile import UpdateMyProfile
from endpoints.get_profile import GetProfile
from endpoints.update_profile import UpdateProfile
from endpoints.delete_profile import DeleteProfile
from endpoints.update_account_role import UpdateAccountRole


@pytest.mark.profile
class TestProfiles:
    #проверка создания профиля
    def test_create_profile_success(self, user_token):
        new_profile_object = CreateProfile()
        payload = {
            'name': 'Иван',
            'surname': 'Иванов',
            'middlename': 'Иванович',
            'birthdate': '2000-01-01',
            'about': 'Тестовый профиль',
            'links': 'link.com'
        }
        new_profile_object.create_profile(payload=payload, token=user_token)
        new_profile_object.check_response_is_201()
        new_profile_object.check_success_message()
        new_profile_object.check_profile_fields(payload)

    #проверка создания профиля, который уже существует
    def test_create_profile_duplicate(self, user_token):
        new_profile_object = CreateProfile()
        payload = {
            'name': 'Дубликат',
            'surname': 'Дубликатов',
            'middlename': 'Дубликатович',
            'birthdate': '2000-01-01',
            'about': 'Дубликатный профиль',
            'links': 'duplicate-link.com'
        }
        new_profile_object.create_profile(payload=payload, token=user_token)
        new_profile_object.check_response_is_201()

        new_profile_object.create_profile(payload=payload, token=user_token)
        new_profile_object.check_response_is_400()
        new_profile_object.check_error_detail_contains('Profile already exists')

    #проверка на то, что пользователь видит в списке только свой профиль
    def test_list_as_user_sees_only_own_profile(self, user_info, user_token):
        #сначала создаем новый профиль
        new_profile_object = CreateProfile()
        payload = {
            'name': 'Тест',
            'surname': 'Тестов',
            'middlename': 'Тестович',
            'birthdate': '2000-01-01',
            'about': 'Тестовый профиль',
            'links': 'test-link.com'
        }
        new_profile_object.create_profile(payload=payload, token=user_token)

        #запрашиваем список профлией
        new_list_object = ListProfiles()
        new_list_object.list_profiles(token=user_token)
        new_list_object.check_response_is_200()
        new_list_object.check_list_contains_user(user_info['id'])
        new_list_object.check_list_contains_only_user()

    #проверка на то, что администратор видит всех пользователей в списке
    def test_list_as_admin_sees_all_profiles(self, admin_token):
        #запрашиваем список профилей от АДМИНА
        new_list_object = ListProfiles()
        new_list_object.list_profiles(token=admin_token)
        new_list_object.check_response_is_200()
        new_list_object.check_list_not_empty()

    #проверка ошибки, в случае запроса с не валидным токеном
    def test_list_unauthorized(self):
        new_list_object = ListProfiles()
        new_list_object.list_profiles(token='invalid_token')
        new_list_object.check_response_is_401()
        new_list_object.check_error_detail_contains('Could not validate credentials')

    #проверка параметров запроса list profiles (limit, offset)
    def test_list_with_limit_offset(self, admin_token):
        #тестовое значение предела
        test_limit = 2
        #сначала проверим работу limit, дальше создадим другой список при помощи изменения
        #значения offset и проверим и его работу
        new_list_object = ListProfiles()
        new_list_object.list_profiles(token=admin_token, limit=test_limit, offset=0)
        new_list_object.check_response_is_200()
        new_list_object.check_list_limit(test_limit)

        new_list_object2 = ListProfiles()
        new_list_object2.list_profiles(token=admin_token, limit=test_limit, offset=1)
        new_list_object2.check_response_is_200()
        #первые элементы должны быть разные (т.к. разный offset)
        if new_list_object.response_json['count'] > 1 and new_list_object2.response_json['count'] > 1:
            id1 = new_list_object.response_json['profiles'][0].get('id')
            id2 = new_list_object2.response_json['profiles'][0].get('id')
            assert id1 != id2
    
    #проверка успешного получения собственного профиля после его создания
    def test_get_my_profile_as_user(self, user_token):
        new_profile_object = CreateProfile()
        payload = {
            'name': 'Тест',
            'surname': 'Тестов',
            'middlename': 'Тестович',
            'birthdate': '2000-01-01',
            'about': 'Тестовый профиль',
            'links': 'test-link.com'
        }
        new_profile_object.create_profile(payload=payload, token=user_token)

        get_my_profile_object = GetMyProfile()
        get_my_profile_object.get_my_profile(token=user_token)
        get_my_profile_object.check_response_is_200()
        get_my_profile_object.check_success_message()
        get_my_profile_object.check_profile_fields(payload)

    #проверка успешного получения профиля администратором
    def test_get_my_profile_as_admin(self, admin_token):
        get_my_profile_object = GetMyProfile()
        get_my_profile_object.get_my_profile(token=admin_token)
        get_my_profile_object.check_response_is_200()
        get_my_profile_object.check_success_message()

    #проверка ошибки, в случае запроса с не валидным токеном
    def test_get_my_profile_unauthorized(self):
        get_my_profile_object = GetMyProfile()
        get_my_profile_object.get_my_profile(token='invalid_token')
        get_my_profile_object.check_response_is_401()
        get_my_profile_object.check_error_detail_contains('Could not validate credentials')

    #проверка успшеного обновления всех полей профиля
    def test_update_my_profile_success(self, user_token):
        #создаем профиль
        new_profile_object = CreateProfile()
        initial_payload = {
            'name': 'Тест',
            'surname': 'Тестов',
            'middlename': 'Тестович',
            'birthdate': '2000-01-01',
            'about': 'Тестовый профиль',
            'links': 'test-link.com'
        }
        new_profile_object.create_profile(payload=initial_payload, token=user_token)

        #обновляем все поля
        new_update_object = UpdateMyProfile()
        new_payload = {
            'name': 'Новый Тест',
            'surname': 'Новый Тестов',
            'middlename': 'Новый Тестович',
            'birthdate': '2001-02-02',
            'about': 'Новый тестовый профиль',
            'links': 'new-test-link.com'
        }
        new_update_object.update_my_profile(token=user_token, payload=new_payload)
        new_update_object.check_response_is_200()
        new_update_object.check_success_message()
        new_update_object.check_updated_fields(new_payload)

    #проверка ошибки, в случае запроса с не валидным токеном
    def test_update_my_profile_unauthorized(self):
        new_update_object = UpdateMyProfile()
        new_update_object.update_my_profile(token='invalid_token', payload={'name': 'test'})
        new_update_object.check_response_is_401()
        new_update_object.check_error_detail_contains('Could not validate credentials')

    #проверка ошибки, в случае обновления еще не созданного профиля
    def test_update_my_profile_not_found(self, user_token):
        new_update_object = UpdateMyProfile()
        new_update_object.update_my_profile(token=user_token, payload={'name': 'test'})
        new_update_object.check_response_is_404() 
        new_update_object.check_error_detail_contains('Profile not found')

    #проверка на получение собственного профиля
    def test_get_own_profile_success(self, user_token, user_info):
        get_profile_object = GetProfile()
        get_profile_object.get_profile(account_id=user_info['id'], token=user_token)
        get_profile_object.check_response_is_200()
        get_profile_object.check_success_message()

    #проверка на то, что админ может получить любой профиль
    def test_admin_can_get_any_profile(self, admin_token, user_info):
        get_profile_object = GetProfile()
        get_profile_object.get_profile(account_id=user_info['id'], token=admin_token)
        get_profile_object.check_response_is_200()
        get_profile_object.check_success_message()

    #проверка на то, что обычный пользователь НЕ может получить любой профиль
    def test_user_cannot_get_other_profile(self, user_token, admin_token):
        #нужно создать второго пользователя для проверки
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
        new_user_object_id = new_user_object.response_json['account']['id']

        #пытаемся получить профиль созданного пользователя первым пользователем
        get_profile_object = GetProfile()
        get_profile_object.get_profile(account_id=new_user_object_id, token=user_token)
        get_profile_object.check_response_is_403()
        get_profile_object.check_error_detail_contains('Permission denied')

        #удаляем второго пользователя, чтобы не засорять БД
        delete_object = DeleteProfile()
        delete_object.delete_profile_by_id(account_id=new_user_object_id,admin_token=admin_token)

    #проверка на получение не существующего пользователя
    def test_get_nonexistent_profile(self, admin_token):
        get_profile_object = GetProfile()
        get_profile_object.get_profile(account_id=999999999, token=admin_token)
        get_profile_object.check_response_is_404()
        get_profile_object.check_error_detail_contains('Profile not found')

    #проверка ошибки, в случае запроса с не валидным токеном
    def test_get_profile_unauthorized(self):
        get_profile_object = GetProfile()
        get_profile_object.get_profile(account_id=1, token='invalid_token')
        get_profile_object.check_response_is_401()
        get_profile_object.check_error_detail_contains('Could not validate credentials')

    #проверка обновления собственного профиля (через запрос api/profiles/{account_id})
    def test_update_own_profile_success(self, user_token, user_info):
        new_profile_object = CreateProfile()
        initial_payload = {
            'name': 'Тест',
            'surname': 'Тестов',
            'middlename': 'Тестович',
            'birthdate': '2000-01-01',
            'about': 'Тестовый профиль',
            'links': 'test-link.com'
        }
        new_profile_object.create_profile(payload=initial_payload, token=user_token)

        new_update_object = UpdateProfile()
        new_payload = {
            'name': 'Новый Тест',
            'surname': 'Новый Тестов',
            'middlename': 'Новый Тестович',
            'birthdate': '2001-02-02',
            'about': 'Новый тестовый профиль',
            'links': 'new-test-link.com'
        }
        new_update_object.update_profile(account_id=user_info['id'], payload=new_payload, token=user_token)
        new_update_object.check_response_is_200()
        new_update_object.check_success_message()
        new_update_object.check_updated_fields(new_payload)

    #проверка но то, что администратор может обновить профиль другого пользователя
    def test_admin_update_any_profile(self, admin_token, user_token, user_info):
        new_profile_object = CreateProfile()
        initial_payload = {
            'name': 'Тест',
            'surname': 'Тестов',
            'middlename': 'Тестович',
            'birthdate': '2000-01-01',
            'about': 'Тестовый профиль',
            'links': 'test-link.com'
        }
        new_profile_object.create_profile(payload=initial_payload, token=user_token)

        new_update_object = UpdateProfile()
        new_payload = {
            'name': 'Новый Тест',
            'surname': 'Новый Тестов',
            'middlename': 'Новый Тестович',
            'birthdate': '2001-02-02',
            'about': 'Новый тестовый профиль',
            'links': 'new-test-link.com'
        }
        new_update_object.update_profile(account_id=user_info['id'], payload=new_payload, token=admin_token)
        new_update_object.check_response_is_200()
        new_update_object.check_success_message()
        new_update_object.check_updated_fields(new_payload)

    #проверка на то, что обычный пользователь НЕ может обновить чужой профиль
    def test_user_cannot_update_other_profile(self, user_token, admin_token):
        #создаем пользователя для теста и регистрируем его
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
        #получили его id
        new_user_object_id = new_user_object.response_json['account']['id']

        #логиним его, чтобы получить его токен
        new_user = LoginUser()
        new_user.login_user({'username': payload['username'], 'password': payload['password']})
        new_user_token = new_user.response_json['access_token']

        #и создаем ему профиль
        new_profile_object = CreateProfile()
        new_user_payload = {
            'name': 'Тест',
            'surname': 'Тестов',
            'middlename': 'Тестович',
            'birthdate': '2000-01-01',
            'about': 'Тестовый профиль',
            'links': 'test-link.com'
        }
        new_profile_object.create_profile(payload=new_user_payload, token=new_user_token)

        #пытаемся онбовить профиль созданного профиля первым пользователем
        new_update_object = UpdateProfile()
        new_update_object.update_profile(account_id=new_user_object_id, payload={'name': 'Хакер'}, token=user_token)
        new_update_object.check_response_is_403()
        new_update_object.check_error_detail_contains('Permission denied')

        #удаляем второго пользователя, чтобы не засорять БД
        delete_object = DeleteProfile()
        delete_object.delete_profile_by_id(account_id=new_user_object_id,admin_token=admin_token)

    #проверка обновления несуществующего профиля
    def test_update_nonexistent_profile(self, admin_token):
        new_update_object = UpdateProfile()
        new_update_object.update_profile(account_id=999999, payload={'name': 'Test'}, token=admin_token)
        new_update_object.check_response_is_404()
        new_update_object.check_error_detail_contains('Profile not found')

    #проверка ошибки, в случае запроса с не валидным токеном
    def test_update_unauthorized(self):
        new_update_object = UpdateProfile()
        new_update_object.update_profile(account_id=1, payload={'name': 'Test'}, token='invalid_token')
        new_update_object.check_response_is_401()
        new_update_object.check_error_detail_contains('Could not validate credentials')

    #проверка на успешное удаление профиля админом
    def test_admin_delete_profile_success(self, admin_token):
        #создаем пользователя для теста и регистрируем его
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
        #получили его id
        new_user_object_id = new_user_object.response_json['account']['id']

        #удаляем профиль
        delete_object = DeleteProfile()
        delete_object.delete_profile_by_id(account_id=new_user_object_id, admin_token=admin_token)
        delete_object.check_response_is_200()
        delete_object.check_success_message()

    #првоерка на то, что обычный пользователь не может удалить профиль
    def test_user_cannot_delete_profile(self, user_token, user_info):
        delete_object = DeleteProfile()
        delete_object.delete_profile_by_id(account_id=user_info['id'], admin_token=user_token)
        delete_object.check_response_is_403()
        delete_object.check_error_detail_contains('Only administrators can delete accounts')

    #проверка ошибки, в случае запроса с не валидным токеном
    def test_delete_unauthorized(self):
        delete_object = DeleteProfile()
        delete_object.delete_profile_by_id(account_id=1, admin_token='invalid_token')
        delete_object.check_response_is_401()
        delete_object.check_error_detail_contains('Could not validate credentials')

    #проверка ошибки, при удалении несуществующего профиля
    def test_delete_nonexistent_profile(self, admin_token):
        delete_object = DeleteProfile()
        delete_object.delete_profile_by_id(account_id=999999, admin_token=admin_token)
        delete_object.check_response_is_500()
        delete_object.check_error_detail_contains('Failed to delete account')

    #проверка на успешную смену роли
    def test_admin_change_role_success(self, admin_token):
        #создаем пользователя для теста и регистрируем его
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
        #получили его id
        new_user_object_id = new_user_object.response_json['account']['id']

        #меняем роль на moderator
        update_role_object = UpdateAccountRole()
        update_role_object.update_role(account_id=new_user_object_id, role_name='moderator', admin_token=admin_token)
        update_role_object.check_response_is_200()
        update_role_object.check_success_message()
        update_role_object.check_id(new_user_object_id)

        #удаляем созданного пользователя, чтобы не засорять БД
        delete_object = DeleteProfile()
        delete_object.delete_profile_by_id(account_id=new_user_object_id,admin_token=admin_token)

    #проверка, что обычный пользователь не может изменять роли
    def test_user_cannot_change_role(self, user_token, user_info):
        update_role_object = UpdateAccountRole()
        update_role_object.update_role(account_id=user_info['id'], role_name='admin', admin_token=user_token)
        update_role_object.check_response_is_403()
        update_role_object.check_error_detail_contains('Only administrators can change roles')

    #проверка ошибки, в случае запроса с не валидным токеном
    def test_change_role_unauthorized(self):
        update_role_object = UpdateAccountRole()
        update_role_object.update_role(account_id=1, role_name='admin', admin_token='invalid_token')
        update_role_object.check_response_is_401()
        update_role_object.check_error_detail_contains('Could not validate credentials')

    #проверка смены роли несуществующему аккаунту
    def test_change_role_nonexistent_account(self, admin_token):
        update_role_object = UpdateAccountRole()
        update_role_object.update_role(account_id=999999, role_name='admin', admin_token=admin_token)
        update_role_object.check_response_is_500()
        update_role_object.check_error_detail_contains('Failed to update role')
        
    #проверка несуществующей роли
    def test_change_role_invalid_role_name(self, admin_token, user_info):
        update_role_object = UpdateAccountRole()
        update_role_object.update_role(account_id=user_info['id'], role_name='superadmin', admin_token=admin_token)
        update_role_object.check_response_is_400()
        update_role_object.check_error_detail_contains('Invalid role name. Must be: user, moderator, or admin')